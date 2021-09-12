from univer_api.tables import Base
from univer_api.database import engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print("БД успешно создана")
