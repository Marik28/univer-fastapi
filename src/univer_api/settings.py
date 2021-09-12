from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = 'localhost'
    server_port: int = 5050

    database_url: str = "sqlite:///../db.sqlite3"

    base_dir: Path = Path(__file__).resolve().parent.parent.parent


settings = Settings()

if not settings.base_dir.exists():
    settings.base_dir.mkdir(parents=True)
