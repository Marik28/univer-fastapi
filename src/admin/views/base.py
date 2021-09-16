from flask_admin.contrib.sqla import ModelView


class BaseModelView(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    can_view_details = True
