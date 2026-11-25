from fastapi import APIRouter,Depends
from core import db,require
from stop_service import Plan,route_board,sign
router=APIRouter(prefix="/circuits")

@router.get("")
def route_stops(_=Depends(require())):
    with db() as cx:
        return route_board(cx)

@router.post("/{code}/plan")
def approve(code:str,data:Plan,user=Depends(require("reviewer"))):
    with db() as cx:
        return sign(cx,code,data,user["email"])
