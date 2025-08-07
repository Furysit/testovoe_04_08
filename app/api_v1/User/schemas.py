from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, List


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=5, max_length=30)

class UserCreate(UserBase):
    password: str = Field(..., min_length=9)
    role: str = Field(..., min_length=4)

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(UserBase):
    id: int
    role: str

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    full_name: Optional[str]
    password: Optional[str]
    role: Optional[str]

class AccountSummary(BaseModel):
    id: int
    name: Optional[str]
    balance: int

    class Config:
        orm_mode = True

class UserWithAccounts(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    role: str
    accounts: List[AccountSummary]

    class Config:
        orm_mode = True