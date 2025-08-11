from datetime import datetime

from sqlalchemy import DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

from app.dao.database import Base


class TronLog(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('Europe/Moscow', NOW())")
    )
    address: Mapped[str] = mapped_column(nullable=False)
    balance: Mapped[float]
    bandwidth: Mapped[int]
    energy: Mapped[int]
