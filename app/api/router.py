from fastapi import APIRouter, Depends

from app.tron.methods import add_address, extract_latest
from app.tron.schemas import AddrPydantic, HistoryPydantic, TronLogPydantic


api_router = APIRouter(prefix="/tron")


@api_router.post("/info")
async def info(data: AddrPydantic) -> TronLogPydantic:
    addr_info = await add_address(data=data)
    return addr_info


@api_router.get("/history")
async def history(hist: HistoryPydantic = Depends()) -> list[TronLogPydantic]:
    list_addrs: list[TronLogPydantic] = await extract_latest(hist=hist)
    return list_addrs
