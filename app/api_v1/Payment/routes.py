from fastapi import APIRouter, Depends, HTTPException, status, Body, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.models import db_helper, User
from typing import List, Optional
from app.core.models import Payment, Account
from .schemas import PaymentCreate, PaymentOut
from . import crud
from app.api_v1.User.dependecies import get_current_user

router = APIRouter(tags=["Payments"])


# PaymentCreate






@router.get("/get_payments_by_account",
           status_code=status.HTTP_200_OK,
           summary="Получить платежи по счету",
           description="Возвращает список платежей для указанного счета пользователя",
           response_model=List[PaymentOut]
           )
async def get_payments_by_account(
    account_id: int,
    user: User = Depends(get_current_user), # Вот тут я бы получал пользователя и потом у него выбирал счет
    session: AsyncSession = Depends(db_helper.get_scoped_session)
) -> List[PaymentOut]:
    stmt = select(Account).where(Account.id == account_id, Account.user_id == user.id)
    result = await session.execute(stmt)
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found or does not belong to user")
    return await crud.get_payments_by_account(account_id=account_id, session=session)

@router.get("/get_payments_by_user",
           status_code=status.HTTP_200_OK,
           summary="Получить платежи по пользователю",
           description="Возвращает список всех платежей по всем счетам пользователя",
           response_model=List[PaymentOut])
async def get_payments_by_user(
    user: User = Depends(get_current_user), 
    session: AsyncSession = Depends(db_helper.get_scoped_session)
) -> List[PaymentOut]:
    return await crud.get_payments_by_user(user_id=user.id, session=session)
