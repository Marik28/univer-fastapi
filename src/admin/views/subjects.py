from univer_api.tables import UsefulLink, Assignment, Lesson
from .base import BaseModelView


class UsefulLinksView(BaseModelView):
    pass


class SubjectsView(BaseModelView):
    inline_models = [Assignment, UsefulLink]
    form_excluded_columns = ["lessons"]
