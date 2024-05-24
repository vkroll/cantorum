from flask import render_template, session, redirect, url_for, jsonify, request
from . import user
from ..models import Login, Person
from ..extensions import db, mail
from flask_mail import Message
from flask_login import login_required, login_user, logout_user, current_user


@user.route('profile')
@login_required
def profile():
    # Get the current user's login data
    login_data = Login.query.filter_by(uuid=current_user.uuid).first()
    print(login_data)
    # Get the associated person data
    person_data = login_data.person
    return render_template('profile.html', person=person_data)

@user.route('list')
@login_required
def userlist():
    persons = Person.query.all()
    return render_template('userlist.html', persons=persons)

@user.route('change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if(request.method == 'POST'):
        data = request.json
        old = data.get('old_password')
        new = data.get('new_password')
        login_data = Login.query.filter_by(uuid=current_user.uuid).first()


        if not old or not new:
            return jsonify({'error': 'Both old and new passwords are required'}), 400

        login_data = Login.query.filter_by(uuid=current_user.uuid).first()

        if login_data is None:
            return jsonify({'error': 'User not found'}), 404

        if not login_data.check_password(old):
            return jsonify({'error': 'Old password is incorrect'}), 401

        login_data.set_password(new)
        db.session.commit()
        return jsonify({'success': 'Password changed successfully'}), 200
    else:
        return render_template('change_pw.html')


    
