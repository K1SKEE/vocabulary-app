from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import settings
from api.schemas import Token, UserCreateForm, UserCreateResponse
from api.utils import Hasher, JWT
from db.managers import UserManager
from db.models import User
from db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def create_new_user(body: UserCreateForm,
                          session: AsyncSession) -> UserCreateResponse | None:
    if body.password_1 != body.password_2:
        return
    hashed_password, salt = Hasher.hash_password(body.password_1)
    async with session.begin():
        user_manager = UserManager(session)
        await user_manager.create_user(
            email=body.email,
            username=body.username,
            hashed_password=hashed_password,
            salt=salt
        )
        return UserCreateResponse(email=body.email)


async def _get_user_for_auth(
        username: str,
        session: AsyncSession) -> User | None:
    async with session.begin():
        user_manager = UserManager(session)
        return await user_manager.get_user(username=username)


async def authenticate_user(username: str,
                            password: str,
                            session: AsyncSession
                            ) -> Token | None:
    user = await _get_user_for_auth(username, session)
    if user is None:
        return
    if not Hasher.check_password(password, user.hashed_password, user.salt):
        return
    _token, _refresh_token = JWT.create_token_for_access(user=user)
    return Token(access_token=_token, refresh_token=_refresh_token)


async def refresh_token_service(user: User) -> Token:
    _token, _refresh_token = JWT.create_token_for_access(user=user)
    return Token(access_token=_token, refresh_token=_refresh_token)


async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_for_auth(username=username, session=db)
    if user is None:
        raise credentials_exception
    if user.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account isn't activated",
        )
    return user
