from sqlalchemy_utils.functions import database_exists, drop_database

from univer_api.database import engine

if __name__ == '__main__':
    db_url = engine.url
    if database_exists(db_url):
        drop_database(db_url)
