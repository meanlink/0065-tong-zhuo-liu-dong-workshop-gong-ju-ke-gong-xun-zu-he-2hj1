from fastapi import HTTPException
from pydantic import BaseModel,Field
from kit_tallies import needs,reconcile

class Plan(BaseModel):
    group:str
    notes:str=Field(min_length=4,max_length=180)

def route_board(cx):
    return cx.execute('''
      SELECT s.*,p.lessons,p.notes,p.signed_by,p.expected_minutes,p.expected_kits FROM road_stops s
      LEFT JOIN stop_plans p ON s.code=p.stop ORDER BY workshop_on
    ''').fetchall()

def sign(cx,key,data,who):
    stop=cx.execute("SELECT * FROM road_stops WHERE code=%s FOR UPDATE",(key,)).fetchone()
    group=cx.execute("SELECT * FROM joint_groups WHERE group_key=%s FOR SHARE",(data.group,)).fetchone()
    if not stop or not group:
        raise HTTPException(409,"驻点或共训组合已失效")
    if cx.execute("SELECT 1 FROM stop_plans WHERE stop=%s",(key,)).fetchone():
        raise HTTPException(409,"驻点已有有效教案")
    selected=cx.execute("SELECT * FROM tool_lessons WHERE code=ANY(%s)",(group["members"],)).fetchall()
    tally=needs(selected)
    issues=reconcile(stop,tally)
    if issues:
        raise HTTPException(409,"、".join(issues))
    cx.execute('''INSERT INTO stop_plans(stop,lessons,expected_minutes,expected_kits,notes,signed_by)
                  VALUES(%s,%s,%s,%s,%s,%s)''',(key,group["members"],tally["minutes"],tally["kits"],data.notes,who))
    return {"stop":key,"lessons":group["members"],**tally}
