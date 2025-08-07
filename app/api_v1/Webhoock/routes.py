from fastapi import APIRouter, Depends, HTTPException, status, Body, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
import hashlib
from sqlalchemy import select
from app.core.models import db_helper, User, Account, Payment
from .schemas import PaymentWebhoock
from app.core.config import settings
from app.api_v1.Account.crud import create_account
from app.api_v1.Account.schemas import AccountCreate
from app.api_v1.Payment.crud import create_payment
from app.api_v1.Payment.schemas import PaymentCreate



router = APIRouter(tags=["Webhoock"])


@router.post("/payment_webhook",
            status_code=status.HTTP_200_OK,
            summary="",
            description="")
async def payment_webhook(
    PaymentWebhoock: PaymentWebhoock,
    session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    sign = f"{PaymentWebhoock.account_id}{PaymentWebhoock.amount}{PaymentWebhoock.transaction_id}{PaymentWebhoock.user_id}{settings.secret_key}"
    hashed_sign = hashlib.sha256(sign.encode()).hexdigest()
    if PaymentWebhoock.signature == hashed_sign:


        # Проверка на уникальность платежки
        stmt = select(Payment).where(Payment.transaction_id == PaymentWebhoock.transaction_id)
        result = await session.execute(stmt)
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Payment with this id already exists"
            )
        

        # Проверка на юзера
        stmt = select(User).where(User.id == PaymentWebhoock.user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exists, payment is scum"
            )
        

        # Проверка на наличие счета
        stmt = select(Account).where(
            Account.id == PaymentWebhoock.account_id,
            Account.user_id == PaymentWebhoock.user_id
            )
        result = await session.execute(stmt)
        account = result.scalar_one_or_none()
        if not account:
            account_in = AccountCreate(
                balance=0,
                name="Новый счет",
                user_id=PaymentWebhoock.user_id
            )
            account = await create_account(session=session, account_in=account_in)

        payment_in = PaymentCreate(
            transaction_id=PaymentWebhoock.transaction_id,
            amount=PaymentWebhoock.amount,
            account_id=account.id
        )
        await create_payment(payment_in=payment_in, session=session)
        
        return {"status": "success", "message": "Payment processed successfully"}
    

