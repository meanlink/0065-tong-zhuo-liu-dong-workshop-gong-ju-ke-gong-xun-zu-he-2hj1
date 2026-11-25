from fastapi import APIRouter,Depends
from pydantic import BaseModel,Field
from card_merges import merge_cards,merge_state
from core import db,enqueue,require
class Pairing(BaseModel):
    threshold:float=Field(gt=0,le=1)
    common:int=Field(ge=2,le=50)

class Merge(BaseModel):
    alias:str=Field(min_length=1,max_length=40)
    primary:str=Field(min_length=1,max_length=40)

router=APIRouter(prefix="/pairings")

@router.get("")
def list_groups(_=Depends(require())):
    with db() as cx:
        return cx.execute("SELECT * FROM joint_groups ORDER BY members").fetchall()

@router.get("/state")
def pairing_state(_=Depends(require())):
    with db() as cx:
        return merge_state(cx)

@router.post("")
def recompute(data:Pairing,_=Depends(require("operator","reviewer"))):
    with db() as cx:
        return {"job_id":enqueue(cx,"shared-attendance",data.model_dump())}

@router.post("/merge")
def merge(data:Merge,user=Depends(require("operator","reviewer"))):
    with db() as cx:
        return merge_cards(cx,data.alias.strip(),data.primary.strip(),user["email"])
