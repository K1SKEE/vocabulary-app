from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api import logger
from api.redis_connectors import RedisConnectors
from api.schemas import Token, UserCreateForm, UserCreateResponse
from api.services.auth_services import (
    authenticate_user, get_current_user_from_token, refresh_token_service,
    create_new_user, send_confirmation_token_to_email,
    confirm_registration_service
)
from db.models import User
from db.session import get_db
from api.utils import EmailClientManager

register_router = APIRouter()
login_router = APIRouter()


@register_router.post("/", response_model=UserCreateResponse)
async def register_user(
        body: UserCreateForm,
        db: AsyncSession = Depends(get_db),
        email_manager: EmailClientManager = Depends(),
        redis: RedisConnectors = Depends()) -> UserCreateResponse:
    try:
        result = await create_new_user(body, db)
        if not result:
            raise HTTPException(status_code=400, detail=f"Паролі не "
                                                        f"співпадають")
        await send_confirmation_token_to_email(body.email, email_manager, redis)
        response_text = f'Підтвердіть аккаунт, повідомлення з посиланням ' \
                        f'відправлено на пошту {result}'
        return UserCreateResponse(response_text=response_text)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503,
                            detail=f"Database error: User already exists.")


@register_router.patch('/activate')
async def confirm_registration(token: str,
                               redis: RedisConnectors = Depends(),
                               db: AsyncSession = Depends(get_db)
                               ) -> Token:
    result = await confirm_registration_service(token, redis, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect user")
    return result


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
