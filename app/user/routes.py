from flask import render_template, session, redirect, url_for
from . import user
from ..models import Login, Person
from ..extensions import db, mail
from flask_mail import Message
from flask_login import login_required, login_user, logout_user, current_user


@user.route('profile')
def profile():
    # Get the current user's login data
    login_data = Login.query.filter_by(uuid=current_user.uuid).first()
    print(login_data)
    # Get the associated person data
    person_data = login_data.person
    return render_template('profile.html', person=person_data)

@user.route('list')
def userlist():
    persons = Person.query.all()
    return render_template('userlist.html', persons=persons)