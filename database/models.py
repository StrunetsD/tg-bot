import asyncio
import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship

from core.config import *

DATABASE_URL = str(ASYNC_DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class UserRole(enum.Enum):
    user = "user"
    superuser = "superuser"
    admin = "admin"
    block = "block"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    chat_id = Column(Integer, unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)
    queries = relationship('UserQuery', back_populates='user', cascade='all, delete-orphan')
    failed_requests = relationship('FailedRequest', back_populates='user', cascade='all, delete-orphan')

    def __str__(self):
        return f"<{self.username}>"


class UserQuery(Base):
    __tablename__ = 'user_queries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    username = Column(String, nullable=False)  # Сохраняем username
    query = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='queries')

    def __str__(self):
        return f"<{self.user_id}, {self.username}, {self.query}, {self.timestamp}>"


class FailedRequest(Base):
    __tablename__ = 'failed_requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    username = Column(String, nullable=False)  # Сохраняем username
    query = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='failed_requests')

    def __str__(self):
        return f"<{self.user_id}, {self.username}, {self.query}, {self.timestamp}>"


async def main():
    await asyncio.sleep(5)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы успешно созданы!")


if __name__ == "__main__":
    asyncio.run(main())