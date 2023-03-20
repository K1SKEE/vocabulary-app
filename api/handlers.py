from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.schemas import UserCreateForm, Token, UserCreateResponse
from api.services import _create_new_user, _authenticate_user
from db.session import get_db

logger = getLogger(__name__)

user_router = APIRouter()
login_router = APIRouter()


@user_router.post("/register", response_model=UserCreateResponse)
async def register_user(body: UserCreateForm,
                        db: AsyncSession = Depends(get_db)
                        ) -> UserCreateResponse:
    try:
        result = await _create_new_user(body, db)
        if not result:
            raise HTTPException(status_code=400, detail=f"Паролі не "
                                                        f"співпадають")
        return result
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@login_router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)) -> Token:
    token = await _authenticate_user(form_data.username,
                                     form_data.password,
                                     db)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    return Token(access_token=token)
