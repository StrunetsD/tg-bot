from sqlalchemy import select

from .models import User, UserQuery, FailedRequest
from .models import async_session

import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("db_log.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


async def set_user(id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == id))

        if not user:
            new_user = User(id=id, username=username, chat_id=id, role='user')
            session.add(new_user)
            await session.commit()
            logger.info(f"Пользователь {username} (ID: {id}) добавлен в базу данных.")
        else:
            logger.info(f"Пользователь {username} (ID: {id}) уже существует в базе данных.")


async def add_user_query(user_id, username, query):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        if user:
            new_request = UserQuery(user_id=user_id, username=username, query=query)
            session.add(new_request)
            await session.commit()
            logger.info(f"Запрос пользователя {username} (ID: {user_id}) добавлен: {query}")
        else:
            logger.error(f"Пользователь {username} (ID: {user_id}) не найден.")
            raise ValueError("User not found")


async def add_failed_user_query(user_id, username, query):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))

        if user:
            failed_request = FailedRequest(user_id=user_id, username=username, query=query)
            session.add(failed_request)
            await session.commit()
            logger.warning(f"Неудачный запрос пользователя {username} (ID: {user_id}) добавлен: {query}")
        else:
            logger.error(f"Пользователь {username} (ID: {user_id}) не найден.")
            raise ValueError("User not found")


async def get_user_role(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        if user:
            logger.info(f"Роль пользователя {user.username} (ID: {user_id}): {user.role}")
            return user.role
        else:
            logger.error(f"Пользователь с ID {user_id} не найден.")
            raise ValueError("User not found")
