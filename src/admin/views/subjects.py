from flask_admin.model.template import macro

from univer_api.tables import (
    UsefulLink,
    Assignment,
)
from .base import BaseModelView


class UsefulLinksView(BaseModelView):
    pass


class SubjectsView(BaseModelView):
    # templates
    details_template = "subjects/details.html"

    # columns
    column_details_list = ["name", "assignments", "useful_links"]
    form_excluded_columns = ["lessons"]

    # formatters
    column_formatters_detail = {
        "useful_links": macro("render_useful_links"),
        "assignments": macro("render_assignments"),
    }

    # customization
    column_default_sort = "name"
    column_searchable_list = ["name"]
    inline_models = [Assignment, UsefulLink]
