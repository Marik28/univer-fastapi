from .base import BaseModelView


class TeachersView(BaseModelView):
    form_excluded_columns = ["lessons"]
