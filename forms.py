from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired ,Email, EqualTo

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
    address = TextAreaField("Address", validators = [])
    submit = SubmitField("Submit")
