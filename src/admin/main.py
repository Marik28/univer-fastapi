from admin.app import create_app
from conf.settings import settings
from univer_api.database import Session

with Session() as session:
    app = create_app(session)
    if __name__ == '__main__':
        app.run(
            host=settings.admin_host,
            port=settings.admin_port,
            debug=settings.debug,
        )
