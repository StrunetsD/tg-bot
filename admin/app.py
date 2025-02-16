import asyncio

from flask_admin import Admin

from database.models import *
from .admin_models import UserAdmin, QueryAdmin, FailedRequestAdmin
from .views import *

admin = Admin(app, name="Admin Panel", template_mode="bootstrap3", index_view=HomeView())

admin.add_view(UserAdmin(User, db.session))
admin.add_view(QueryAdmin(UserQuery, db.session))
admin.add_view(FailedRequestAdmin(FailedRequest, db.session))


async def main():
    await asyncio.sleep(5)
    db_exists = await check_database_exists()

    if not db_exists:
        await create_tables()

    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    asyncio.run(main())
