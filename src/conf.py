import os
from os import path
from dotenv import load_dotenv

load_dotenv()

_db_url = os.getenv("DATABASE_URL")
if _db_url and _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql://", 1)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = _db_url or (
        "sqlite:///" + path.join(path.dirname(__file__), "test.db")
    )
    UPLOAD_PATH = path.join(path.dirname(__file__), "static", "uploads")
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True} if _db_url else {}


class TestConf(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(
        path.dirname(__file__), "pytest.db"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {}
    TESTING = True