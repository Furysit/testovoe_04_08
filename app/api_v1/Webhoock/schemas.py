from pydantic import BaseModel, Field
from uuid import UUID

class PaymentWebhoock(BaseModel):
    transaction_id: UUID
    user_id: int
    account_id: int
    amount: int = Field(..., gt=0)
    signature: str = Field(..., min_length=64, max_length=64)