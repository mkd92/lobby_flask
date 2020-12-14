from app import app,hash_password, User,db, user_loader, login_manager,Properties, Units, Transactions
from forms import LoginForm, SignupForm, AddProperty, TransactionForm
from flask import Flask, render_template, url_for, request, redirect, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from datetime import date, datetime, timezone
from sqlalchemy.exc import SQLAlchemyError

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
    if request.method =='POST':
        if add_property_form.validate_on_submit():
            title = add_property_form.title.data
            address = add_property_form.address.data
            user_id = current_user.id
            new_property = Properties(title=title, address=address, user_id=user_id)
            try:
                db.session.add(new_property)
                db.session.commit()
                return redirect(url_for('dashboard'))
            except:
                return "There was a problem adding property"
        for error in add_property_form.errors:
            print (error)
            
    
    return render_template("dashboard.html",add_property_form = add_property_form, current_user = current_user)

@app.route('/dashboard/units/<int:prop_id>', methods = ['GET','POST'])
@login_required
def units(prop_id):
    print(request)
    session['prop_id'] = prop_id
    add_property_form = AddProperty()
    units = Units.query.filter_by(user_id = current_user.id, property_id = prop_id)
    if request.method == 'POST':
        if add_property_form.validate_on_submit():
            title = add_property_form.title.data
            detail = add_property_form.address.data
            user_id = current_user.id
            prop_id = prop_id
            new_unit = Units(title = title, detail = detail, user_id = user_id, property_id = prop_id)
            try:
                db.session.add(new_unit)
                db.session.commit()
                return redirect(url_for('units', prop_id = prop_id))
            except:
                return "there was a problem"
    return render_template("units.html", add_property_form = add_property_form, current_user = current_user, prop_id = prop_id, units = units)

@app.route('/dashboard/units/<int:prop_id>/transactions/<int:unit_id>', methods=['POST','GET'])
@login_required
def transactions(prop_id, unit_id):
    transaction_form = TransactionForm()
    units = Units.query.filter_by(user_id = current_user.id, property_id = prop_id)
    transactions = Transactions.query.filter_by(user_id = current_user.id, property_id = prop_id, unit_id = unit_id)
    if request.method == 'POST':
        if transaction_form.validate_on_submit():
            date_added = request.form.get('tran_date')
            if date_added:
                date_added = date_added.replace('T', ' ')
                date_added = datetime.strptime(date_added, '%Y-%m-%d %H:%M')
            else:
                date_added = datetime.now()
            amount = transaction_form.amount.data
            amount = round(amount, 2)
            detail = transaction_form.detail.data
            new_transaction = Transactions(date_added = date_added, amount = amount, detail = detail, user_id = current_user.id, property_id = prop_id, unit_id = unit_id)
            try:
                db.session.add(new_transaction)
                db.session.commit()
                return redirect(url_for('transactions', transaction_form = transaction_form, prop_id=prop_id, unit_id=unit_id, units = units,current_user = current_user, transactions = transactions))
            except SQLAlchemyError as e:
                return str(e.__dict__['orig'])
        print(transaction_form.errors,transaction_form.date_added.data)
    return render_template("transactions.html",transaction_form = transaction_form, prop_id=prop_id, unit_id=unit_id, units = units,current_user = current_user, transactions = transactions)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "You are Logged out"

@app.route('/add_property')
@login_required
def add_property():
    return render_template("add_property.html")