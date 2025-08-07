from fastapi import APIRouter, Depends, HTTPException, status, Body, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import db_helper, User
from typing import List, Optional
from .schemas import AccountCreate, AccountOut, AccountBase
from fastapi import status
from . import crud
from app.api_v1.User.dependecies import get_current_user


router = APIRouter(tags=["Account"])

@router.post("/create_account",
             status_code=status.HTTP_201_CREATED,
             summary="Создать новый счет",
             description="Создает новый счет авторизованному пользователю")
async def create_account(
    account_name: Optional[str] = Query(None, description="Название счета"),
    session: AsyncSession = Depends(db_helper.get_scoped_session),
    user: User = Depends(get_current_user),
):
    account_in = AccountCreate(
        balance=0,
        name=account_name or AccountBase.model_fields['name'].default,
        user_id=user.id
    )
    return await crud.create_account(session=session, account_in=account_in)

@router.get("/get_my_accounts",
            status_code=status.HTTP_200_OK,
            summary="Получить список счетов",
            description="Возвращает список всех счетов пользователя",
            response_model=List[AccountOut])
async def get_my_accounts(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.get_scoped_session)
) -> List[AccountOut]:
    return await crud.get_accounts_by_user(session=session, user_id=user.id)
    