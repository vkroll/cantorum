from .extensions import db
import uuid
from sqlalchemy.dialects.mysql import BINARY
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from sqlalchemy import Enum, event


# Helper function to generate UUID
def generate_uuid():
    return uuid.uuid4().bytes

# Models
login_roles = db.Table('login_roles',
    db.Column('login_uuid', db.String(36), db.ForeignKey('login.uuid'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)
class Login(db.Model):
    __tablename__ = 'login'
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    # Relationships
    person = db.relationship('Person', backref='login', lazy=True)
    loginattempts = db.relationship('LoginAttempts', backref='login', lazy=True)
    roles = db.relationship('Role', secondary=login_roles, lazy='subquery',
                            backref=db.backref('logins', lazy=True))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

def insert_initial_roles(*args, **kwargs):
    db.session.add_all([
        Role(name='admin'),
        Role(name='singer'),
        Role(name='viewer'),
        Role(name='conductor'),
        Role(name='choir board'),
        Role(name='assistent'),
        Role(name='correpetitor'),
        Role(name='voice trainer')
        # Add other roles as necessary
    ])
    db.session.commit()

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    login_uuid = db.Column(db.String(36), db.ForeignKey('login.uuid'))
    vorname = db.Column(db.String(50), nullable=False)
    nachname = db.Column(db.String(50), nullable=False)

class State(enum.Enum):
    MEMBER = 'member'
    GUEST = 'guest'
    VACATION = 'vacation'

class Voice(db.Model):
    __tablename__= 'voice'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(128))

def insert_initial_voices(*args, **kwargs):
    db.session.add_all([
        Voice(name = "S1", description = "Sopran 1"),
        Voice(name = "S2", description = "Sopran 2"),
        Voice(name = "A1", description = "Alt 1"),
        Voice(name = "A2", description = "Alt 2"),
        Voice(name = "T1", description = "Tenor 1"),
        Voice(name = "T2", description = "Tenor 2"),
        Voice(name = "B1", description = "Bass 1"),
        Voice(name = "B2", description = "Bass 2")
        # Add other roles as necessary
    ])
    db.session.commit()   

class Singer(db.Model):
    __tablename__ = 'singer'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    voice_id = db.Column(db.Integer, db.ForeignKey('voice.id'))
    state = db.Column(Enum(State),default=State.MEMBER)



class LoginAttempts(db.Model):
    __tablename__ = 'loginattempts'
    id = db.Column(db.Integer, primary_key=True)
    login_uuid = db.Column(db.String(36), db.ForeignKey('login.uuid'))
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
    start_date = db.Column(db.Date, nullable=False)  # Start date of the event
    end_date = db.Column(db.Date)  # End date of the event (can be null for single-day events)
    start_time = db.Column(db.Time, nullable=False)  # Start time (considering same start time for all days)
    end_time = db.Column(db.Time)  # End time (considering same end time for all days)
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


# Listening to the 'after_create' event
event.listen(Role.__table__, 'after_create', insert_initial_roles)
event.listen(Voice.__table__, 'after_create', insert_initial_voices)