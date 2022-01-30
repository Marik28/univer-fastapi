from flask_admin.model.template import macro

from .base import BaseModelView


class GroupsBaseView(BaseModelView):
    # templates
    details_template = "groups/details.html"

    # columns
    form_excluded_columns = ["lessons", "assignments", "students"]
    column_details_list = ["name", "assignments"]
    # formatters
    column_formatters_detail = {
        "assignments": macro("render_assignments"),
    }
