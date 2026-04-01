from fastapi import APIRouter
from typing import List
from models.vattu import TonKho
from crud import tonkho as crud_tonkho

router = APIRouter(prefix="/tonkho", tags=["Tồn Kho"])

@router.get("/global", response_model=List[TonKho])
async def read_global():
    return crud_tonkho.get_tonkho_global()

@router.get("/{site}", response_model=List[TonKho])
async def read_by_site(site: str):
    return crud_tonkho.get_tonkho_by_site(site)