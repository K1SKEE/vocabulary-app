from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)

    vocabulary = relationship('Dictionary', backref='user')


class Dictionary(Base):
    __tablename__ = 'dictionary'

    eng = Column(String, nullable=False)
    ukr = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
