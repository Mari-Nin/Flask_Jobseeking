
import pytest
from src import create_app
from src.conf import TestConf
from src.commands import init_db,populate_db
from src.ext import admin

@pytest.fixture()
def app():
    app = create_app(TestConf)

    admin._views = []
    with app.app_context():
        init_db()
        populate_db()
        yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.cli_runner(app)
