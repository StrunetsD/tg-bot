import enum
import asyncio
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from config import *

DATABASE_URL = str(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine)



class Base(DeclarativeBase, AsyncAttrs):
    pass


class UserRole(enum.Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String, unique=True, nullable=False)
    chat_id = Column(Integer, unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)
    playlists = relationship('Playlist', back_populates='user')

    def __str__(self):
        return self.username


class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    playlists = relationship('PlaylistMusic', back_populates='music')

    def __str__(self):
        return self.title


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='playlists')
    music = relationship('PlaylistMusic', back_populates='playlist')

    def __str__(self):
        return self.name


class PlaylistMusic(Base):
    __tablename__ = 'playlist_music'

    id = Column(Integer, primary_key=True, autoincrement=True)
    playlist_id = Column(Integer, ForeignKey('playlists.id'))
    music_id = Column(Integer, ForeignKey('music.id'))
    playlist = relationship('Playlist', back_populates='music')
    music = relationship('Music', back_populates='playlists')


async def main():
    await asyncio.sleep(5)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы успешно созданы!")


if __name__ == "__main__":
    asyncio.run(main())
