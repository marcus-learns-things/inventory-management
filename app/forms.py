from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, length

# User Registration form with simple validation of data input using wtforms.
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class InventoryItemForm(FlaskForm):
    name = StringField('ItemName', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Add Item')
    item_name = StringField('ItemName', validators=[DataRequired()])
    item_price = StringField('ItemPrice', validators=[DataRequired()])
    submit = SubmitField('Add Item')

