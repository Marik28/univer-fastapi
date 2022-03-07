import sqlalchemy.orm
from flask import Flask
from flask_admin import Admin
from flask_basicauth import BasicAuth

from conf.settings import settings

basic_auth = BasicAuth()


# TODO: refactor
def create_app(session: sqlalchemy.orm.Session) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.flask_secret_key
    app.config['BASIC_AUTH_USERNAME'] = settings.basic_auth_username
    app.config['BASIC_AUTH_PASSWORD'] = settings.basic_auth_password

    basic_auth.init_app(app)

    admin = Admin(app, name="univer_api", template_mode="bootstrap4", url=settings.admin_url)

    from univer_api.tables import Assignment, UsefulLink, Subject, Lesson, Group, Teacher

    from .views.assignments import AssignmentsView
    admin.add_view(AssignmentsView(Assignment, session))

    from .views.subjects import UsefulLinksView
    admin.add_view(UsefulLinksView(UsefulLink, session))

    from .views.subjects import SubjectsView
    admin.add_view(SubjectsView(Subject, session))

    from .views.lessons import LessonsView
    admin.add_view(LessonsView(Lesson, session))

    from .views.groups import GroupsBaseView
    admin.add_view(GroupsBaseView(Group, session))

    from .views.teachers import TeachersView
    admin.add_view(TeachersView(Teacher, session))

    return app
