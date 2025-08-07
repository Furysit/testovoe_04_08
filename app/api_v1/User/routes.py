from fastapi import APIRouter, Depends, HTTPException, status, Body, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.models import db_helper, User
from .schemas import UserCreate, UserOut, UserUpdate, UserWithAccounts, AccountSummary
from fastapi import status
from . import crud
from .auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from .dependecies import get_current_user, admin_required



router = APIRouter(tags=["User"])

@router.post("/login",
             status_code=status.HTTP_200_OK,
             summary="Авторизация",
             description="Авторизует пользователя и отправляет токен в заголовке")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    user = await crud.auth_user(session=session, email=form_data.username, password=form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token,
            "token_type": "bearer",
            "user" : {
                "id" : user.id,
                "email" : user.email,
                "role" : user.role
            }}

@router.get("/get_my_info",
            status_code=status.HTTP_200_OK,
            response_model=UserOut,
            summary="Получить информацию о себе",
            description="Возвращает id, email, роль авторизованного пользователя")
async def get_my_info(
    user: User = Depends(get_current_user),
):
    return user

@router.post("/admin/create_user",
             status_code=status.HTTP_201_CREATED,
             summary="Создание пользователя",
             description="Доступно только авторизованному админу")
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.get_scoped_session),
    admin: User = Depends(admin_required)
):
    return await crud.create_user(session=session, user_in=user_in)


@router.delete("/admin/delete_user",
               status_code=status.HTTP_204_NO_CONTENT,
               response_model=None,
               summary="Удаление юзера",
               description="Доступно только авторизованному админу")
async def delete_user(
    user_email : str ,
    session : AsyncSession = Depends(db_helper.get_scoped_session),
    admin: User = Depends(admin_required)
):
    await crud.delete_user(user_email=user_email, session=session)

@router.put("/admin/users/{user_id}",
            response_model=UserOut,
            summary="Обновить пользователя",
            description="Обновляет данные пользователя")
async def update_user_route(
    user_id: int,
    user_in: UserUpdate,
    session: AsyncSession = Depends(db_helper.get_scoped_session),
    admin: User = Depends(admin_required)
):
    user = await crud.update_user(session=session, user_id=user_id, user_in=user_in)
    return user

@router.get("/admin/users_with_accounts",
            response_model=List[UserWithAccounts],
            summary="Список пользователей с их счетами")
async def get_users_with_accounts_route(
    session: AsyncSession = Depends(db_helper.get_scoped_session),
    admin: User = Depends(admin_required)
):
    users = await crud.get_users_with_accounts(session=session)
    return users