from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = 'localhost'
    server_port: int = 5050

    flask_secret_key: str

    base_dir: Path = Path(__file__).resolve().parent.parent.parent

    database_url: str = f"sqlite:///{base_dir / 'db.sqlite3'}"


settings = Settings()

if not settings.base_dir.exists():
    settings.base_dir.mkdir(parents=True)
