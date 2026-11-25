"""同一学员的副卡合入正卡：签到归正卡，并按原门槛触发共训组合重算。

并发约定：
- 合卡与后台重算共用顾问锁 35017（pairing_results.run_job 也持有它），
  保证“查到重算任务状态”和“决定是否需要补一个新任务”之间不会被交错。
- 合卡与补录各自先锁学员卡（合卡按卡号升序锁两张），补录在锁内重读
  card_merges，因此合卡提交前后的签到都不会丢。
"""
from fastapi import HTTPException

from core import enqueue

RECOMPUTE_KIND = "shared-attendance"


def hold_job(cx):
    """仍在排队或运行的合卡重算任务；它存在期间暂停签发新教案。"""
    return cx.execute("""
        SELECT id,status FROM app_jobs
        WHERE kind=%s AND status IN ('queued','running')
          AND COALESCE((payload->>'hold')::boolean,false)
        ORDER BY id LIMIT 1
    """, (RECOMPUTE_KIND,)).fetchone()


def _original_params(cx):
    """产出当前组合的最近一次成功计算所用的门槛。"""
    row = cx.execute(
        "SELECT payload FROM app_jobs WHERE kind=%s AND status='done' ORDER BY id DESC LIMIT 1",
        (RECOMPUTE_KIND,)).fetchone()
    if not row:
        return None
    payload = row["payload"]
    return {"threshold": payload["threshold"], "common": payload["common"]}


def merge_state(cx):
    return {
        "held": hold_job(cx) is not None,
        "merges": cx.execute(
            "SELECT alias,primary_code,merged_by,merged_at FROM card_merges ORDER BY alias"
        ).fetchall(),
        "last_merge_job": cx.execute("""
            SELECT id,status,error,finished_at FROM app_jobs
            WHERE kind=%s AND COALESCE((payload->>'hold')::boolean,false)
            ORDER BY id DESC LIMIT 1
        """, (RECOMPUTE_KIND,)).fetchone(),
    }


def merge_cards(cx, alias, primary, who):
    if alias == primary:
        raise HTTPException(409, "正卡和副卡不能是同一张")
    cx.execute("SELECT pg_advisory_xact_lock(35017)")
    for code in sorted((alias, primary)):  # 按卡号升序锁定，避免与补录或其他合卡互相等待成环
        if not cx.execute("SELECT 1 FROM pupil_cards WHERE code=%s FOR UPDATE", (code,)).fetchone():
            raise HTTPException(409, f"学员卡 {code} 不存在")
    existing = cx.execute("SELECT * FROM card_merges WHERE alias=%s", (alias,)).fetchone()
    if existing and existing["primary_code"] != primary:
        raise HTTPException(409, f"副卡 {alias} 已合入 {existing['primary_code']}，不能改合其他正卡")
    if existing:
        message = f"副卡 {alias} 已合入 {primary}，重复合卡不会重复计人"
    else:
        if cx.execute("SELECT 1 FROM card_merges WHERE alias=%s", (primary,)).fetchone():
            raise HTTPException(409, f"{primary} 本身已作为副卡合出，请直接合到最终正卡")
        if cx.execute("SELECT 1 FROM card_merges WHERE primary_code=%s", (alias,)).fetchone():
            raise HTTPException(409, f"{alias} 已是其他副卡的正卡，不能再作为副卡")
        cx.execute(
            "INSERT INTO card_merges(alias,primary_code,merged_by) VALUES(%s,%s,%s)",
            (alias, primary, who))
        # 同课同日有一张已签收就算签收。
        cx.execute("""
            INSERT INTO module_attendance(pupil,lesson,seen,checked)
            SELECT %s,lesson,seen,checked FROM module_attendance WHERE pupil=%s
            ON CONFLICT(pupil,lesson,seen) DO UPDATE
            SET checked=module_attendance.checked OR excluded.checked
        """, (primary, alias))
        moved = cx.execute("DELETE FROM module_attendance WHERE pupil=%s", (alias,)).rowcount
        message = f"已把副卡 {alias} 合入正卡 {primary}，归并 {moved} 条签到"

    params = _original_params(cx)
    if params is None:
        return {"message": message, "job_id": None}
    running = hold_job(cx)
    if running:
        return {"message": message + "；共训组合重算进行中", "job_id": running["id"]}
    job_id = enqueue(cx, RECOMPUTE_KIND, {**params, "hold": True, "reason": "card-merge"})
    return {"message": message + "；已按原门槛重算共训组合，算完前暂停签发", "job_id": job_id}
