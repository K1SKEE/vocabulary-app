from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api import logger
from api.schemas import Token, UserCreateResponse, UserCreateForm
from api.services.auth_services import (
    authenticate_user, get_current_user_from_token, refresh_token_service,
    create_new_user
)
from db.models import User
from db.session import get_db

register_router = APIRouter()
login_router = APIRouter()


@register_router.post("/", response_model=UserCreateResponse)
async def register_user(body: UserCreateForm,
                        db: AsyncSession = Depends(get_db)
                        ) -> UserCreateResponse:
    try:
        result = await create_new_user(body, db)
        if not result:
            raise HTTPException(status_code=400, detail=f"Паролі не "
                                                        f"співпадають")
        return result
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503,
                            detail=f"Database error: User already exists.")


@login_router.post("/", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)) -> Token:
    token = await authenticate_user(form_data.username,
                                    form_data.password,
                                    db)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    return token


@login_router.post('/refresh', response_model=Token)
async def refresh_token(
        current_user: User = Depends(get_current_user_from_token)) -> Token:
    return await refresh_token_service(current_user)
