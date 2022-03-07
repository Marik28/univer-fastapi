from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import redirect

from admin.app import basic_auth
from admin.auth import AuthException


class BaseModelView(ModelView):
    can_delete = True
    can_edit = True
    can_create = True
    can_view_details = True

    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())
