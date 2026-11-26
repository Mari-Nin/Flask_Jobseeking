import os
from os import path
from dotenv import load_dotenv


load_dotenv()

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= 'sqlite:///' + path.join(path.dirname(__file__),'test.db')
    UPLOAD_PATH = path.join(path.dirname(__file__), 'static', 'uploads')


class TestConf(Config):
    SQLALCHEMY_DATABASE_URI= 'sqlite:///' + path.join(path.dirname(__file__),'pytest.db')
    TESTING = True
    