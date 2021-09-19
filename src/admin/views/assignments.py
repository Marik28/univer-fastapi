from univer_api.models.groups import Subgroup
from .base import BaseModelView
from ..services import make_choices


class AssignmentsView(BaseModelView):
    form_choices = {
        "subgroup": make_choices(Subgroup),
    }
