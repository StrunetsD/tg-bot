from .models import async_session
from .models import User, UserRole, Music, Playlist, PlaylistMusic
from sqlalchemy import select, update, delete


async def set_user(id, username ):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == id))

        if not user:
            if not user:

                new_user = User(id=id, username=username, chat_id=id, role='user')
                session.add(new_user)
                await session.commit()
                print(f"Пользователь {username} добавлен в базу данных.")
