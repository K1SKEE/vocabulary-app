from logging import getLogger

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import UserCreate
from api.services import _create_new_user
from db.session import get_db

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/register", response_model=UserCreate)
async def register_user(body: UserCreate,
                        db: AsyncSession = Depends(get_db)) -> UserCreate:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
