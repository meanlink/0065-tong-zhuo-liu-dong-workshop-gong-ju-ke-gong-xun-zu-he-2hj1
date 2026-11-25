from psycopg.types.json import Jsonb
from jaccard_graph import communities

def run_job(cx,kind,payload):
    if kind!="shared-attendance":
        raise ValueError(kind)
    cx.execute("SELECT pg_advisory_xact_lock(35017)")
    sets={}
    for row in cx.execute('''
          SELECT a.lesson,a.pupil FROM module_attendance a JOIN pupil_cards p ON a.pupil=p.code
          WHERE a.checked AND p.pass='active' ORDER BY lesson,pupil
    '''):
        sets.setdefault(row["lesson"],set()).add(row["pupil"])
    groups=communities(sets,payload["threshold"],payload["common"])
    cx.execute("DELETE FROM joint_groups")
    for members,evidence in groups:
        cx.execute("INSERT INTO joint_groups(group_key,members,min_support,evidence) VALUES(%s,%s,%s,%s)",
                   ("/".join(members),members,min(edge["ratio"] for edge in evidence),Jsonb(evidence)))
    return {"groups":[members for members,_ in groups],"included_lessons":len(sets)}
