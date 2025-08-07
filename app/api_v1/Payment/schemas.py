from pydantic import BaseModel, Field
import uuid
class PaymentBase(BaseModel):
    amount: int = Field(..., gt=0, description="Сумма пополнения баланса в целых единицах")

class PaymentCreate(PaymentBase):
    transaction_id: uuid.UUID
    account_id: int  

class PaymentOut(PaymentBase):
    id: int
    account_id: int

    class Config:
        from_attributes = True
