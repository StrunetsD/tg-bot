from flask_admin.contrib.sqla import ModelView


class UserAdmin(ModelView):
    column_list = ['id', 'username', 'chat_id', 'role']
    form_columns = ['username', 'chat_id', 'role']
    column_filters = ['role']
    column_searchable_list = ['username', 'chat_id']
    column_editable_list = ['role']
    can_edit = True
    can_delete = True
    can_create = False


class QueryAdmin(ModelView):
    column_list = ['id', 'user_id', 'username', 'query', 'timestamp']
    form_columns = ['user_id', 'username', 'query']
    column_filters = ['timestamp']
    column_searchable_list = ['username', 'query']
    can_delete = True
    can_create = False
    can_edit = False


class FailedRequestAdmin(ModelView):
    column_list = ['id', 'user_id', 'username', 'query', 'timestamp']
    form_columns = ['user_id', 'username', 'query']
    column_filters = ['timestamp']
    column_searchable_list = ['username', 'query']
    can_delete = True
    can_create = False
    can_edit = False
