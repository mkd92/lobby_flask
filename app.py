from flask import Flask, render_template, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from datetime import datetime, timezone
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bluebird92'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

def hash_password(pw):
    return generate_password_hash(pw)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True, index=True)
    username = db.Column(db.String(60), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    properties = db.relationship('Properties', backref='properties_owner', lazy = True)
    units = db.relationship('Units', backref='units_owner', lazy = True)
    transactions = db.relationship('Transactions', backref='transactions_owner', lazy = True)

    def check_password(self,pw):
        return check_password_hash(self.password_hash,pw)
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class Properties(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(60), index = True, nullable = False)
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    address = db.Column(db.String(120), index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    unit_id = db.relationship('Units',backref='units_property', lazy = True)
    transaction_id = db.relationship('Transactions',backref='transactions_property', lazy = True)


    def __repr__(self):
        return f"Properties('{self.title}','{self.address}')"

class Units(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(60), index = True, nullable = False)
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    detail = db.Column(db.String(120), index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'),nullable = False)
    transactions = db.relationship('Transactions',backref='transactions_unit', lazy = True)
    def __repr__(self):
        return f"Units('{self.title}','{self.detail}')"

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float, nullable = False)
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    detail = db.Column(db.String(120), index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'),nullable = False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'),nullable = False)
    def __repr__(self):
        return f"Transactions('{self.date_added}','{self.detail}')"



@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))

if __name__ == '__main__':
    app.run(debug=True)
    sess = Session()
    sess.init_app(app)

import routes