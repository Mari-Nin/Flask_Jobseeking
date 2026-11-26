from flask_wtf import FlaskForm
from wtforms.fields import SelectField,FileField,IntegerField,DecimalField,StringField,SubmitField
from wtforms.validators import DataRequired,NumberRange
from flask_wtf.file import FileAllowed


class IpekForm(FlaskForm):
    category=SelectField('Category', choices=[],coerce=int,validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    stock = IntegerField('quantity', validators=[DataRequired()]) 
    img = FileField("Image",validators=[FileAllowed(['jpg', 'png', 'jpeg','avif','webp'],)])
    

    submit = SubmitField('Add')

class ShoppingForm(FlaskForm):
    id=IntegerField('Product ID')
    name = StringField('Name')
    price = DecimalField('Price')
    stock = IntegerField('Available quantity') 
    quantity = IntegerField('Enter quantity',validators=
                    [DataRequired
                    (message='Please enter quantity'),
                    NumberRange(min=1, message='Quantity must be greater than 0')
                        ])

    submit = SubmitField('Shop')


    



