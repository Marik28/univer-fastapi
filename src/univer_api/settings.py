from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = 'localhost'
    server_port: int = 5050

    database_url: str = "sqlite:///../db.sqlite3"

    base_dir: Path = Path.cwd().parent


settings = Settings()
