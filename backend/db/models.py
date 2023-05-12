from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, Boolean, LargeBinary
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    salt = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean(), default=False)

    vocabulary = relationship('Dictionary', backref='user')


class Dictionary(Base):
    __tablename__ = 'dictionary'

    id = Column(Integer, primary_key=True)
    eng = Column(String, nullable=False)
    ukr = Column(String, nullable=False)
    flag = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
