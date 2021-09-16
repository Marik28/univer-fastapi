from flask_admin import Admin

from univer_api.database import Session
from univer_api.settings import settings
from univer_api.tables import Assignment, UsefulLink
from .app import app
from .views.assignments import AssignmentsView
from .views.subjects import UsefulLinksView

admin = Admin(app, name="univer_api", template_mode="bootstrap4", url=settings.admin_url)

with Session() as session:
    admin.add_view(AssignmentsView(Assignment, session))
    admin.add_view(UsefulLinksView(UsefulLink, session))
    if __name__ == '__main__':
        app.run()
