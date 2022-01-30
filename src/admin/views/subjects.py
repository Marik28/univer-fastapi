from flask_admin.model.template import macro

from univer_api.tables import (
    UsefulLink,
    Assignment,
)
from .base import BaseModelView


class UsefulLinksView(BaseModelView):
    pass


class SubjectsView(BaseModelView):
    inline_models = [Assignment, UsefulLink]
    column_details_list = ["name", "assignments", "useful_links"]
    form_excluded_columns = ["lessons"]
    details_template = "subjects/details.html"
    column_formatters_detail = {
        "useful_links": macro("render_useful_links"),
        "assignments": macro("render_assignments"),
    }
