from .tables import Base
from .database import engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)