from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import UserCreate
from db.managers import UserManager
from api.utils import hash_password


async def _create_new_user(body: UserCreate,
                           session: AsyncSession) -> UserCreate:
    async with session.begin():
        user_manager = UserManager(session)
        hashed_password, salt = hash_password(body.password)
        await user_manager.create_user(
            username=body.username,
            hashed_password=hashed_password,
            salt=salt
        )
        return UserCreate(username=body.username,
                          password=body.password)
