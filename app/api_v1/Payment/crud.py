from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, update
from .schemas import PaymentCreate
from app.core.models import Payment
from app.core.models import Account
from app.core.models import User


async def create_payment(
        payment_in: PaymentCreate,
        session: AsyncSession
):
    payment = Payment(
        transaction_id = payment_in.transaction_id,
        amount = payment_in.amount,
        account_id = payment_in.account_id
    )
    session.add(payment)

    stmt = select(Account).where(Account.id == payment_in.account_id)
    result = await session.execute(stmt)
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    account.balance += payment.amount
    await session.commit()
    await session.refresh(payment)
    return payment


async def get_payments_by_account(
        account_id: int,
        session: AsyncSession
):
    stmt = select(Payment).where(Payment.account_id == account_id)
    payments = await session.execute(stmt).scalars().all()
    return payments


async def get_payments_by_user(
        user_id: int,
        session: AsyncSession
):
    stmt = select(Payment).join(Account, Payment.account_id == Account.id).where(Account.user_id == user_id)
    payments = await session.execute(stmt).scalars().all()
    return payments