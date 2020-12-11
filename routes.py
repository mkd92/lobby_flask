from app import app,hash_password, User,db, user_loader, login_manager
from forms import LoginForm, SignupForm, AddProperty
from flask import Flask, render_template, url_for, request, redirect
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user


@app.route('/',)
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            user = User.query.filter_by(username = login_form.username.data).first()
            if user:
                if user.check_password(login_form.password.data):
                    login_user(user)
                    print('loggedin')
                    return redirect(url_for('dashboard'))
    return render_template("login.html", login_form=login_form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    if request.method == 'POST':
        if signup_form.validate_on_submit():
            username = signup_form.username.data
            email = signup_form.email.data
            password_hash = hash_password(signup_form.password.data)
            new_user = User(username = username, email = email, password_hash = password_hash) 
            
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))

            except:
                return "there is an issue with logging in"
    
    return render_template("signup.html", signup_form=signup_form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    add_property_form = AddProperty()
    
    return render_template("dashboard.html",add_property_form = add_property_form )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "You are Logged out"

@app.route('/add_property')
@login_required
def add_property():
    return render_template("add_property.html")