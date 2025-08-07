from fastapi import APIRouter
import hashlib
import uuid
from app.core.config import settings

router = APIRouter(tags=["Test Webhook"])


@router.get("/generate_webhook_json")
async def generate_webhook_json(
    account_id: int,
    user_id: int,
    amount: int
):
    transaction_id = str(uuid.uuid4())
    
    # Формируем подпись в алфавитном порядке ключей
    sign_string = f"{account_id}{amount}{transaction_id}{user_id}{settings.secret_key}"
    signature = hashlib.sha256(sign_string.encode()).hexdigest()
    
    webhook_payload = {
        "transaction_id": transaction_id,
        "user_id": user_id,
        "account_id": account_id,
        "amount": amount,
        "signature": signature
    }
    
    return webhook_payload