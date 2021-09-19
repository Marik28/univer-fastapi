from .base import BaseModelView


class GroupsBaseView(BaseModelView):
    form_excluded_columns = ["lessons", "assignments"]
