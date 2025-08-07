from pydantic import BaseModel, Field
from typing import Optional

class AccountBase(BaseModel):
    balance: int = Field(0, ge=0, description="Баланс счета")
    name: Optional[str] = Field("Основной счет", max_length=100)

class AccountCreate(AccountBase):
    user_id: int

class AccountUpdate(BaseModel):
    balance: Optional[int] = Field(None, ge=0)
    name: Optional[str] = Field(None, max_length=100)

class AccountOut(AccountBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

