from flask import render_template,redirect,url_for,Blueprint,request
from flask_login import logout_user,login_user

from src.views.auth.forms import RegisterForm,LoginForm
from src.models.user import User



auth_bp = Blueprint('register',__name__)
@auth_bp.route('/register',methods=["GET","POST"])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        username=User(name =form.username.data,password = form.password.data )
        username.create()
        return redirect(url_for('main.index'))
    
    else:
        print(form.errors)
        return render_template('auth/register.html',form=form)

login_bp = Blueprint('login',__name__)
@login_bp.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username=User.query.filter_by(name =form.username.data).first()
        login_user(username)
        if request.args.get('next'):
            return redirect(request.args.get('next'))
                
        return redirect(url_for('main.index'))

    else:
        print(form.errors)
    return render_template('auth/login.html',form=form)


@login_bp.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('main.index'))




            