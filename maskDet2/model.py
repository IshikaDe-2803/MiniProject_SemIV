from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import os

basedir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(basedir, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

  

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(120), primary_key=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.Unicode(255), nullable=False)
    def __init__(self, email=None, password=None, telephone=None):
        self.email = email
        self.password = password
        self.telephone = telephone

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.Unicode(255), nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    def __init__(self, username=None, email=None, telephone=None, message=None):
        self.username = username
        self.email = email
        self.telephone = telephone
        self.message = message

