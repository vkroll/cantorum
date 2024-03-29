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

class EventType(db.Model):
    __tablename__ = 'event_types'

    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(100))  # Description for the event type

    # Relationship to Event
    events = db.relationship('Event', backref='event_type', lazy=True)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_types.id'), nullable=False)

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Primary name, e.g., 'Marien-Kirche'

    # Relationship to Room
    rooms = db.relationship('Room', backref='location', lazy=True)

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Name of the room
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)

    # Relationship to Event
    events = db.relationship('Event', backref='room', lazy=True)
