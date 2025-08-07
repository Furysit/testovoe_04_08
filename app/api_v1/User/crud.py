from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from app.core.models import User, Account
from .schemas import UserCreate, UserUpdate, UserWithAccounts, AccountSummary
from .auth import hash_password, verify_password

# Создание пользователя
async def create_user(
        session: AsyncSession,
        user_in: UserCreate
):
    stmt = select(User).where(User.email == user_in.email)
    result : Result = await session.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that email already exists"
        )

    hashed_password = await hash_password(user_in.password)
    user = User(
        email = user_in.email,
        full_name = user_in.full_name,
        hashed_password = hashed_password,
        role = user_in.role
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    account = Account(
        name="Основной счет",
        balance=0,
        user_id=user.id
    )
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return user

# Получить пользователя по ID
async def get_user_by_id(
        session: AsyncSession,
        user_id: int
):
    stmt = select(User).where(User.id == user_id)
    result : Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with that id does not exist"
        )
    return user

# Получить пользователя по EMAIL, сделано для того, чтобы админ мог удалять пользователя по email
async def get_user_by_email(
        user_email : str,
        session: AsyncSession
):
    stmt = select(User).where(User.email == user_email)
    result : Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email does not exist"
        )
    return user

async def auth_user(
        session: AsyncSession,
        email: str,
        password: str
):
    stmt = select(User).where(User.email == email)
    result : Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    if not verify_password(plain_password=password, hashed = user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not valid password"
        )
    return user

async def delete_user(
        user_email: str,
        session: AsyncSession
):
    user = await get_user_by_email(user_email=user_email, session=session)
    await session.delete(user)
    await session.commit()

async def update_user(
    session: AsyncSession,
    user_id: int,
    user_in: UserUpdate
):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with that id does not exist"
        )

    if user_in.email:
        user.email = user_in.email
    if user_in.full_name:
        user.full_name = user_in.full_name
    if user_in.password:
        user.hashed_password = hash_password(user_in.password) # Оставил синхронной 
    if user_in.role:
        user.role = user_in.role

    await session.commit()
    await session.refresh(user)
    return user


async def get_users_with_accounts(
        session: AsyncSession
):
    stmt = select(User).options(selectinload(User.accounts))
    result = await session.execute(stmt)
    users = result.scalars().unique().all()
    return users