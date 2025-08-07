from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, update
from .schemas import AccountCreate
from app.core.models import Account
from app.core.models import User


async def create_account(
        session: AsyncSession,
        account_in: AccountCreate
):
    # Проверяем, что пользователь существует
    stmt = select(User).where(User.id == account_in.user_id)
    result: Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    account = Account(
        user_id=account_in.user_id,
        balance=account_in.balance,
        name=account_in.name
    )
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account

async def get_accounts_by_user(
        session: AsyncSession,
        user_id: int
):
    stmt = select(Account).where(Account.user_id == user_id)
    result: Result = await session.execute(stmt)
    return result.scalars().all()