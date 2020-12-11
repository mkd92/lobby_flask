from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators 

class LoginForm(FlaskForm):
    email = StringField("E-mail", [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])
    submit = SubmitField("Submit")

class SignupForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    email = StringField("E-mail", [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])
    re_password = PasswordField("Confirm Password", [validators.
                                DataRequired(), validators.EqualTo(password)])
    submit = SubmitField("Submit")
