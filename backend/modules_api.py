from fastapi import APIRouter,Depends
from core import db,require
from education_catalog import lesson_index

router=APIRouter(prefix="/modules")

@router.get("")
def list_modules(_=Depends(require())):
    with db() as cx:
        return lesson_index(cx)
