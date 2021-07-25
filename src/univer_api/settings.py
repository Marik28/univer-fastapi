from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = 'localhost'
    server_port: int = 5050

    database_url: str = "sqlite:///./db.sqlite3"


settings = Settings()
