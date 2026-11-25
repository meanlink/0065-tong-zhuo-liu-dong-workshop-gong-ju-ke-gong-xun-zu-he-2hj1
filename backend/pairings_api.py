from fastapi import APIRouter,Depends
from pydantic import BaseModel,Field
from core import db,enqueue,require
class Pairing(BaseModel):
    threshold:float=Field(gt=0,le=1)
    common:int=Field(ge=2,le=50)

router=APIRouter(prefix="/pairings")

@router.get("")
def list_groups(_=Depends(require())):
    with db() as cx:
        return cx.execute("SELECT * FROM joint_groups ORDER BY members").fetchall()

@router.post("")
def recompute(data:Pairing,_=Depends(require("operator","reviewer"))):
    with db() as cx:
        return {"job_id":enqueue(cx,"shared-attendance",data.model_dump())}
