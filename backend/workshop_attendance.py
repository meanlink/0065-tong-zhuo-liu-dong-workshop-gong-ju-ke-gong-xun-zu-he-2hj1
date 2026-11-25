from datetime import date
from fastapi import HTTPException
from pydantic import BaseModel

class Checkin(BaseModel):
    pupil:str
    lesson:str
    seen:date
    checked:bool

def evidence(cx):
    pupils=cx.execute("SELECT * FROM pupil_cards ORDER BY code").fetchall()
    checked=cx.execute("SELECT * FROM module_attendance ORDER BY seen DESC,pupil,lesson").fetchall()
    merges=cx.execute("SELECT alias,primary_code,merged_by,merged_at FROM card_merges ORDER BY alias").fetchall()
    return {"pupils":pupils,"attendance":checked,"merges":merges}

def record(cx,item):
    # 先锁被刷的卡，与合卡互斥：合卡提交前的补录随合卡一并归并，提交后的补录直接落到正卡。
    person=cx.execute("SELECT * FROM pupil_cards WHERE code=%s FOR UPDATE",(item.pupil,)).fetchone()
    if not person:
        raise HTTPException(409,"学员教育卡不存在")
    merged=cx.execute("SELECT primary_code FROM card_merges WHERE alias=%s",(item.pupil,)).fetchone()
    target=person
    if merged:
        target=cx.execute("SELECT * FROM pupil_cards WHERE code=%s",(merged["primary_code"],)).fetchone()
    if target["pass"]!="active":
        raise HTTPException(409,"临访教育卡已失效，不能算作签到证据")
    if item.seen<target["joined"]:
        raise HTTPException(409,"签到日在学员开卡前")
    cx.execute('''
        INSERT INTO module_attendance VALUES(%s,%s,%s,%s)
        ON CONFLICT(pupil,lesson,seen) DO UPDATE SET checked=excluded.checked
    ''',(target["code"],item.lesson,item.seen,item.checked))
    if merged:
        return {"message":f"副卡 {item.pupil} 已合入正卡 {target['code']}，签到归正卡"}
    return {"message":"签到已更新"}
