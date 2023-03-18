from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


class UserManager:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, username: str, hashed_password: str,
                          salt: str) -> User:
        new_user = User(
            username=username,
            hashed_password=hashed_password,
            salt=salt
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
