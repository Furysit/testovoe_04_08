from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.models import db_helper
from .auth import SECRET_KEY, ALGORITHM
from . import crud
from app.core.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api_v1/login")  


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await crud.get_user_by_id(session=session, user_id=int(user_id))
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User with that id does not exist"
    )


async def admin_required(
        user: User = Depends(get_current_user)
)-> User:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only for admins"
        )
    return user