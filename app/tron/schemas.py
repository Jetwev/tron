from pydantic import BaseModel, ConfigDict, Field, field_validator


class TronLogPydantic(BaseModel):
    address: str
    balance: float
    bandwidth: int
    energy: int

    model_config = ConfigDict(from_attributes=True)


class AddrPydantic(BaseModel):
    address: str

    @field_validator("address")
    def start_with_T_and_length(cls, value: str) -> str:
        if not value.startswith("T"):
            raise ValueError("Address must start with 'T'")
        return value


class HistoryPydantic(BaseModel):
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=10, ge=1)
