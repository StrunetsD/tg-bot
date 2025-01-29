import factory
from sqlalchemy.ext.asyncio import AsyncSession

from .models import *

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = AsyncSession(engine)

    username = factory.Faker('user_name')
    chat_id = factory.Faker('random_int', min=10000, max=99999)
    title = factory.Faker('sentence', nb_words=3)
    file_path = factory.Faker('file_path', extension='mp3')


async def fill_database():
    async with AsyncSession(engine) as session:
        async with session.begin():

            user1 = UserFactory.build()
            user2 = UserFactory.build()
            session.add_all([user1, user2])

        await session.commit()
        print("База данных успешно заполнена!")


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await fill_database()


if __name__ == "__main__":
    asyncio.run(main())