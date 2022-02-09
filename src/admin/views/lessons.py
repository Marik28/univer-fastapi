from univer_api.models.lessons import Subgroup, LessonKind, WeekDay, Parity
from .base import BaseModelView
from ..services import make_choices


class LessonsView(BaseModelView):
    column_searchable_list = ("subject.name", "teacher.first_name", "teacher.second_name", "teacher.middle_name")
    column_list = ["subject", "group", "kind", "day"]
    form_choices = {
        "subgroup": make_choices(Subgroup),
        "kind": make_choices(LessonKind),
        "day": make_choices(WeekDay),
        "parity": make_choices(Parity),
    }
