# app/services/user_service.py

from ..extensions import db
from ..models import Login,Person, Singer
from sqlalchemy.exc import IntegrityError
from sys import stderr

def register_user(username, email, password):
    try:
        new_user = Login(username=username, email=email)
        new_user.set_password(password)  # Assuming you have a method to hash passwords
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except IntegrityError:
        db.session.rollback()
        print('Error in generation of user', file=stderr)
        return None
    
def add_person_data(email, vorname, nachname):
    user = Login.query.filter_by(email=email).first()
    person = Person(vorname = vorname, nachname = nachname, login = user)
    db.session.add(person)
    db.session.commit()
    
    return person

def add_singer(vorname, nachname, username, email, voice_id):
    try:
        new_login = Login(username=username, email=email)
        new_login.set_password('defaultpassword')
        new_person = Person(login=new_login, vorname=vorname, nachname=nachname)
        new_singer = Singer(person=new_person, voice_id=voice_id)
        db.session.add(new_login)
        db.session.add(new_person)
        db.session.add(new_singer)
        db.session.commit()    
        return new_singer
    except IntegrityError:
        db.session.rollback()
        return None
    