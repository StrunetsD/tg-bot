import factory
from sqlalchemy.ext.asyncio import AsyncSession

from models import *


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = AsyncSession(engine)

    username = factory.Faker('user_name')
    chat_id = factory.Faker('random_int', min=10000, max=99999)

class MusicFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Music
        sqlalchemy_session = AsyncSession(engine)

    title = factory.Faker('sentence', nb_words=3)
    file_path = factory.Faker('file_path', extension='mp3')

class PlaylistFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Playlist
        sqlalchemy_session = AsyncSession(engine)

    name = factory.Faker('sentence', nb_words=2)
    user = factory.SubFactory(UserFactory)


async def fill_database():
    async with AsyncSession(engine) as session:
        async with session.begin():

            user1 = UserFactory.build()
            user2 = UserFactory.build()


            music1 = MusicFactory.build()
            music2 = MusicFactory.build()


            playlist1 = PlaylistFactory.build(user=user1)
            playlist2 = PlaylistFactory.build(user=user2)

            session.add_all([user1, user2, music1, music2, playlist1, playlist2])

        await session.commit()
        print("База данных успешно заполнена!")


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await fill_database()


if __name__ == "__main__":
    asyncio.run(main())