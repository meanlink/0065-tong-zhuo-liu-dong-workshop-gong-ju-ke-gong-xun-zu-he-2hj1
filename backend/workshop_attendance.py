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
    return {"pupils":pupils,"attendance":checked}

def record(cx,item):
    person=cx.execute("SELECT * FROM pupil_cards WHERE code=%s",(item.pupil,)).fetchone()
    if not person or person["pass"]!="active":
        raise HTTPException(409,"临访教育卡已失效，不能算作签到证据")
    if item.seen<person["joined"]:
        raise HTTPException(409,"签到日在学员开卡前")
    cx.execute('''
        INSERT INTO module_attendance VALUES(%(pupil)s,%(lesson)s,%(seen)s,%(checked)s)
        ON CONFLICT(pupil,lesson,seen) DO UPDATE SET checked=excluded.checked
    ''',item.model_dump())
    return {"message":"签到已更新"}
