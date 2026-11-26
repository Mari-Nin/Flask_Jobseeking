from flask_admin.contrib.sqla import ModelView
from flask import redirect,url_for,request
from flask_login import current_user
from flask_admin import AdminIndexView

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login.login',next=request.url))

class SecureIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
        #return False   -  ყველანაირ წვდომას უზღუდავს ადმინს  -  forbidden

    def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('login.login',next=request.url))