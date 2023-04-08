from typing import List

from sqlalchemy import select, update, and_, delete, func
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
        query = (
            select(User)
            .where(User.username == username)
        )
        result = await self.db_session.execute(query)
        user_data = result.fetchone()
        if user_data is not None:
            return user_data[0]

    async def get_user_vocabulary(self, username: str,
                                  limit: int = 100,
                                  offset: int = 0) -> List[Dictionary]:
        query = (
            select(Dictionary)
            .join(User)
            .where(User.username == username)
            .limit(limit)
            .offset(offset)
            .order_by(Dictionary.id.asc())
        )
        result = await self.db_session.execute(query)
        return [row[0] for row in result.fetchall()]

    async def get_count_vocabulary(self, username: str) -> int:
        query = (
            select(func.count(Dictionary.id))
            .join(User)
            .where(User.username == username)
        )
        result = await self.db_session.execute(query)
        return result.scalar()

    async def get_user_vocabulary_for_repetition(
            self, username: str) -> List[Dictionary]:
        query = (
            select(Dictionary)
            .join(User)
            .where(and_(User.username == username,
                        Dictionary.flag == True))
        )
        result = await self.db_session.execute(query)
        return [row[0] for row in result.fetchall()]


class DictionaryManager:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_to_vocabulary(self, eng: str, ukr: str,
                                user: User) -> Dictionary:
        new_word = Dictionary(eng=eng, ukr=ukr, user_id=user.user_id)
        self.db_session.add(new_word)
        await self.db_session.flush()
        return new_word

    async def update_vocabulary(self, word_id: int, user_id: int,
                                **kwargs) -> Dictionary:
        query = (
            update(Dictionary)
            .where(and_(Dictionary.user_id == user_id,
                        Dictionary.id == word_id))
            .values(kwargs)
            .returning(Dictionary)
        )
        result = await self.db_session.execute(query)
        row = result.fetchone()
        if row is not None:
            return row[0]

    async def delete_word_from_vocabulary(
            self, word_id: int, user_id: int) -> None:
        query = (
            delete(Dictionary)
            .where(and_(Dictionary.user_id == user_id,
                        Dictionary.id == word_id))
        )
        await self.db_session.execute(query)
        await self.db_session.commit()
