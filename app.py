from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bluebird92'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

def hash_password(pw):
    return generate_password_hash(pw)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True, index=True)
    username = db.Column(db.String(60), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    
@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))

if __name__ == '__main__':
    app.run(debug=True)

import routes