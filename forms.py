from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, DecimalField,DateField
from wtforms.validators import DataRequired ,Email, EqualTo, Optional
from datetime import datetime, date




class LoginForm(FlaskForm):
    username = StringField("E-mail", validators =[DataRequired()])
    password = PasswordField("Password",validators = [DataRequired()])
    submit = SubmitField("Submit")

class SignupForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("E-mail", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    re_password = PasswordField("Confirm Password",validators = [
                                DataRequired(), EqualTo('password')])
    submit = SubmitField("Submit")
    
class AddProperty(FlaskForm):
    title = StringField("Title", validators = [DataRequired()])
    address = TextAreaField("Address", validators = [Optional()])
    submit = SubmitField("Submit")

class TransactionForm(FlaskForm):
    amount = DecimalField("Some USD Number", number_format="#,##0.00 USD", validators = [ DataRequired()])
    date_added = DateField('Transaction Date', default= date.today)
    detail = StringField("Details", validators=[DataRequired()])