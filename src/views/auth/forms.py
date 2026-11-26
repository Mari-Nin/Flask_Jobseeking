from flask_wtf.form import FlaskForm
from werkzeug.security import check_password_hash
from wtforms.validators import DataRequired,EqualTo,ValidationError
from string import ascii_uppercase,ascii_lowercase,digits,punctuation
from wtforms.fields import PasswordField,SelectField,FileField,IntegerField,DecimalField,StringField,SubmitField,SelectField,BooleanField

from src.models.user import User


class RegisterForm(FlaskForm):
    username = StringField('Name and surname',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2=PasswordField('Repeat password',validators=[DataRequired(),EqualTo('password',message='Passwords do not match')])
    countries = SelectField('Choose country',choices=[('GE','Georgia'),('GER','Germany'),('ITL','Italy')],validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Register')

    def validate_password(self,field):
            has_lower =False
            has_upper=False
            has_digit=False
            has_punctuation=False
    
            for char in field.data:
                if char in ascii_lowercase:
                    has_lower=True
                if char in ascii_uppercase:
                    has_upper=True
                if char in digits:
                    has_digit=True
                if char in punctuation:
                    has_punctuation = True

            password_parts=[]
    
            if not has_lower:
                password_parts.append('Include a lowercase letter')
            if not has_upper:
                password_parts.append('Include an uppercase letter')
            if not has_digit:
                password_parts.append('Include a digit')
            if not has_punctuation:
                password_parts.append('Include a special character')
            
    
            if password_parts:
                  error_message = f"Password missing: {', '.join(password_parts)}"
                  raise ValidationError(error_message)
            
    def validate_username(self,field):
        existing_user = User.query.filter_by(name = field.data).first()
        if existing_user:
            raise ValidationError('Invalid user')
                
class LoginForm(FlaskForm):
    username = StringField('Name and surname',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_username(self,field):
        username=User.query.filter_by(name=field.data).first()
                            
        if not username:
            raise ValidationError('Invalid username or password. Please try again or go to another page')

    def validate_password(self, field):
        username = User.query.filter_by(name=self.username.data).first()

                                                                                                                                                                                                                                                                                                                                                                                     
