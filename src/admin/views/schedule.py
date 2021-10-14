from univer_api.settings import settings
from .base import BaseModelView


class ScheduleView(BaseModelView):
    list_template = str(settings.base_dir / "templates" / "schedule.html")
