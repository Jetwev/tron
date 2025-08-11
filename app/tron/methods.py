from sqlalchemy.ext.asyncio import AsyncSession

from app.tron.dao import TronLogDAO
from app.tron.schemas import AddrPydantic, HistoryPydantic, TronLogPydantic
from app.utils.session_maker import connection
from app.utils.tron_info import get_address_info


@connection(commit=True)
async def add_address(session:AsyncSession, data: AddrPydantic) -> TronLogPydantic:
    addr_info = await get_address_info(data.address)
    instance = await TronLogDAO.add(session=session, data=addr_info)
    return TronLogPydantic.model_validate(instance)


@connection(commit=False)
async def extract_latest(session: AsyncSession, hist: HistoryPydantic) -> list[TronLogPydantic]:
    list_instances = await TronLogDAO.extract(session=session, page=hist.page, per_page=hist.per_page)
    return [TronLogPydantic.model_validate(inst) for inst in list_instances]
