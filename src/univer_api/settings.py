from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = 'localhost'
    server_port: int = 5050
    debug: bool = True

    flask_secret_key: str
    admin_url: str = '/univer/admin/'
    basic_auth_username: str = "admin"
    basic_auth_password: str = "admin"

    base_dir: Path = Path(__file__).resolve().parent.parent.parent

    database_url: str = f"sqlite:///{base_dir / 'db.sqlite3'}"


settings = Settings()

if not settings.base_dir.exists():
    settings.base_dir.mkdir(parents=True)
