from flask_admin import Admin

from univer_api.database import Session
from univer_api.tables import Assignment, UsefulLink
from .app import app
from .views.assignments import AssignmentsView
from .views.subjects import UsefulLinksView

admin = Admin(app, name="univer_api", template_mode="bootstrap4")

with Session() as session:
    admin.add_view(AssignmentsView(Assignment, session))
    admin.add_view(UsefulLinksView(UsefulLink, session))
    app.run()
