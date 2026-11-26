from flask_sqlalchemy  import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restx import Api
from flask_admin import Admin
from src.admin_views.base import SecureIndexView



db=SQLAlchemy()

migrate = Migrate()
login_manager=LoginManager()
admin = Admin(name = 'Ipekyol', index_view=SecureIndexView())
api = Api(prefix='/api', version='1.0', title='Ipekyol API',doc='/docs')




