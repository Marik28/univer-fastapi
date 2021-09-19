from flask_admin import Admin

from univer_api.database import Session
from univer_api.settings import settings
from univer_api.tables import Assignment, UsefulLink, Subject, Lesson, Group, Teacher
from .app import app
from .views.assignments import AssignmentsView
from .views.groups import GroupsBaseView
from .views.lessons import LessonsView
from .views.subjects import UsefulLinksView, SubjectsView
from .views.teachers import TeachersView

admin = Admin(app, name="univer_api", template_mode="bootstrap4", url=settings.admin_url)

with Session() as session:
    admin.add_view(AssignmentsView(Assignment, session))
    admin.add_view(UsefulLinksView(UsefulLink, session))
    admin.add_view(SubjectsView(Subject, session))
    admin.add_view(LessonsView(Lesson, session))
    admin.add_view(GroupsBaseView(Group, session))
    admin.add_view(TeachersView(Teacher, session))
    if __name__ == '__main__':
        app.run()
