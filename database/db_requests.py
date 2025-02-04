from sqlalchemy import select

from .models import User, UserQuery, FailedRequest
from .models import async_session


async def set_user(id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == id))

        if not user:
            if not user:
                new_user = User(id=id, username=username, chat_id=id, role='user')
                session.add(new_user)
                await session.commit()
                print(f"Пользователь {username} добавлен в базу данных.")


async def add_user_query(user_id, username, query):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        if user:
            new_request = UserQuery(user_id=user_id, username=username, query=query)
            session.add(new_request)
            await session.commit()
        else:
            raise ValueError("User not found")


async def add_failed_user_query(user_id, username, query):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        if user:
            failed_request = FailedRequest(user_id=user_id, username=username, query=query)
            session.add(failed_request)
            await session.commit()
        else:
            raise ValueError("User not found")
