from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = 'localhost'
    server_port: int = 5050
    debug: bool = True

    flask_secret_key: str
    admin_url: str = '/univer/admin/'
    basic_auth_username: str
    basic_auth_password: str
    admin_host: str = 'localhost'
    admin_port: int = 5000

    base_dir: Path = Path(__file__).resolve().parent.parent

    database_url: str


settings = Settings()
