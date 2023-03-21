from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Dictionary


class UserManager:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, username: str, hashed_password: str,
                          salt: bytes) -> User:
        new_user = User(
            username=username,
            hashed_password=hashed_password,
            salt=salt
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def get_user(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        result = await self.db_session.execute(query)
        user_data = result.fetchone()
        if user_data is not None:
            return user_data[0]


class DictionaryManager:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_to_vocabulary(
            self, eng: str,
            ukr: str,
            user: User) -> Dictionary:
        new_word = Dictionary(
            eng=eng,
            ukr=ukr,
            user_id=user.user_id
        )
        self.db_session.add(new_word)
        await self.db_session.flush()
        return new_word
