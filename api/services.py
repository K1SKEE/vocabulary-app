from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import UserCreateForm, UserCreateResponse, Token
from db.managers import UserManager
from db.models import User
from api.utils import Hasher, create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def _create_new_user(body: UserCreateForm,
                           session: AsyncSession) -> UserCreateResponse | None:
    if body.password_1 != body.password_2:
        return
    hashed_password, salt = Hasher.hash_password(body.password_1)
    async with session.begin():
        user_manager = UserManager(session)
        await user_manager.create_user(
            username=body.username,
            hashed_password=hashed_password,
            salt=salt
        )
        return UserCreateResponse(username=body.username,
                                  password=body.password_1)


async def _get_user_for_auth(
        username: str,
        session: AsyncSession) -> User | None:
    async with session.begin():
        user_manager = UserManager(session)
        return await user_manager.get_user(username=username)


async def _authenticate_user(username: str,
                             password: str,
                             session: AsyncSession
                             ) -> Token | None:
    user = await _get_user_for_auth(username, session)
    if user is None:
        return
    if not Hasher.check_password(password, user.hashed_password, user.salt):
        return
    token = create_access_token(user=user)
    return token
