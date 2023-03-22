from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.schemas import (
    UserCreateForm, Token, UserCreateResponse, AddWordResponse, AddWordForm
)
from api.services import (
    _create_new_user, _authenticate_user, get_current_user_from_token,
    _add_new_word, _get_vocabulary
)
from db.models import User
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


@user_router.post('/add', response_model=AddWordResponse)
async def add_new_word_to_vocabulary(
        body: AddWordForm,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> AddWordResponse | None:
    return await _add_new_word(body, current_user, db)


@user_router.get('/vocabulary')
async def get_vocabulary(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    return await _get_vocabulary(user=current_user, session=db)
