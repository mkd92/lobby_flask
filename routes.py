from app import app,hash_password
from forms import LoginForm, SignupForm
from flask import Flask, render_template, url_for, request, redirect


@app.route('/',)
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    return render_template("login.html", login_form=login_form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        email = signup_form.email.data
        password_hash = hash_password(signup_form.password.data)
    
    return render_template("signup.html", signup_form=signup_form)
