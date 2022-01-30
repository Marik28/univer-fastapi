from flask_admin.model.template import macro

from univer_api.models.groups import Subgroup
from .base import BaseModelView
from ..services import make_choices


class AssignmentsView(BaseModelView):
    # templates
    list_template = "assignments/list.html"

    # columns
    column_list = ["title", "subject", "complete_before", "is_important", "archived"]
    column_editable_list = ["archived"]

    # formatters
    column_formatters = {
        "subject": macro("render_subject"),
    }

    # customization
    form_choices = {
        "subgroup": make_choices(Subgroup),
    }
    column_default_sort = "complete_before"
    column_searchable_list = ["title", "subject.name"]
