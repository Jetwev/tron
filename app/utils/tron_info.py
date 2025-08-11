from tronpy import AsyncTron

from app.config import settings
from app.tron.schemas import TronLogPydantic


async def get_address_info(address: str) -> TronLogPydantic:
    async with AsyncTron(network=settings.NETWORK) as client:
        balance = await client.get_account_balance(address)
        bandwidth = await client.get_bandwidth(address)
        energy = await client.get_energy(address)
        return TronLogPydantic(address=address, balance=balance, bandwidth=bandwidth, energy=energy)
