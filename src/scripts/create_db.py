from sqlalchemy_utils.functions import database_exists, create_database

from univer_api.database import engine
from univer_api.tables import Base

if __name__ == '__main__':
    db_url = engine.url
    if not database_exists(db_url):
        create_database(db_url)
        Base.metadata.create_all(engine)
        print("БД успешно создана")
