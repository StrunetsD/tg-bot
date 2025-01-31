from flask_admin import Admin
from admin_models import UserAdmin, QueryAdmin, FailedRequestAdmin
from views import *

admin = Admin(app, name="Admin Panel", template_mode="bootstrap3", index_view=HomeView())

admin.add_view(UserAdmin(User, db.session))
admin.add_view(QueryAdmin(UserQuery, db.session))
admin.add_view(FailedRequestAdmin(FailedRequest, db.session))


if __name__ == '__main__':
    app.run(debug=True)
