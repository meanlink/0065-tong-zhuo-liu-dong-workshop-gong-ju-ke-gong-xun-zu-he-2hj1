from fastapi import APIRouter,Depends
from core import db,require
from workshop_attendance import Checkin,evidence,record
router=APIRouter(prefix="/checkins")

@router.get("")
def checkins(_=Depends(require())):
    with db() as cx:
        return evidence(cx)

@router.post("")
def check_in(item:Checkin,_=Depends(require("operator","reviewer"))):
    with db() as cx:
        return record(cx,item)
