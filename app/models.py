from . import db
import uuid
from sqlalchemy.dialects.mysql import BINARY

# Helper function to generate UUID
def generate_uuid():
    return uuid.uuid4().bytes

# Models
class Login(db.Model):
    __tablename__ = 'login'
    uuid = db.Column(BINARY(16), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # Relationships
    person = db.relationship('Person', backref='login', lazy=True)
    loginattempts = db.relationship('LoginAttempts', backref='login', lazy=True)

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    login_uuid = db.Column(BINARY(16), db.ForeignKey('login.uuid'), nullable=False)
    vorname = db.Column(db.String(50), nullable=False)
    nachname = db.Column(db.String(50), nullable=False)

class LoginAttempts(db.Model):
    __tablename__ = 'loginattempts'
    id = db.Column(db.Integer, primary_key=True)
    login_uuid = db.Column(BINARY(16), db.ForeignKey('login.uuid'), nullable=False)
    last_login = db.Column(db.DateTime)
    failed_login_attempts = db.Column(db.Integer, default=0)