from flask import Flask
from src.conf import Config
from src.ext import db,login_manager,migrate,admin,api

from src.endpoints.product.ipek import IpekAPI
from src.endpoints.auth.auth import LoginApi
from src.endpoints.auth.auth import auth_ns
from src.models.user import User
from src.views.main.routes import main_bp
from src.views.auth.routes import auth_bp,login_bp
from src.views.product.routes import ipek_bp
from src.commands import init_db_command,populate_db_command
from src.models.product import Category,IpekItems
from src.admin_views.base import SecureModelView
from src.admin_views.product import IpekView,CategoryView
from src.admin_views.user import UserView


blueprints = [main_bp,auth_bp,ipek_bp,login_bp]
commands=[init_db_command,populate_db_command]


def create_app(config=Config):
    app = Flask(__name__,static_folder='static')
    
    app.config.from_object(config)
    
    register_blueprints(app)
    register_commands(app)
    register_extentions(app)
    return app

def register_extentions(app):
     db.init_app(app)
     migrate.init_app(app,db)
     login_manager.init_app(app)
     login_manager.login_view = 'login.login'

     @login_manager.user_loader
     def load_user(id):
          return User.query.get(int(id))

     api.init_app(app)

     admin.init_app(app)

     admin.add_view(UserView(User, db.session))
     admin.add_view(CategoryView(Category, db.session))
     admin.add_view(IpekView(IpekItems, db.session))


def register_blueprints(app):
    for blueprint in blueprints:
            app.register_blueprint(blueprint)

def register_commands(app):
     for command in commands:
          app.cli.add_command(command)

