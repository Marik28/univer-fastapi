from flask import Flask
from flask_admin import Admin

from univer_api.database import Session
from univer_api.settings import settings
from univer_api.tables import Assignment, UsefulLink
from .views.assignments import AssignmentsView
from .views.subjects import UsefulLinksView

app = Flask(__name__)
app.config["SECRET_KEY"] = settings.flask_secret_key
admin = Admin(app, name="univer_api", template_mode="bootstrap4")
if __name__ == '__main__':
    with Session() as session:
        admin.add_view(AssignmentsView(Assignment, session))
        admin.add_view(UsefulLinksView(UsefulLink, session))
        app.run()
