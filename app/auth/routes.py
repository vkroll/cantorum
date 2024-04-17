from flask import render_template, session, redirect, url_for
from . import auth
from .forms import RegistrationForm,LoginForm
from .helper import update_login_attempt
from ..models import Login
from ..extensions import db, mail
from flask_mail import Message
from flask_login import login_required, login_user, logout_user



@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Login(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # Redirect to login page:

    return render_template('auth/register_user.html', title="Register User", form=form)

@auth.route('/protected')
@login_required
def protected_route():
    # This route requires authentication
    # Only authenticated users will reach here
    return 'You are logged in!'

@auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session['user_id'] = str(user.uuid)
            update_login_attempt(user.uuid, True) 
            # Redirect to the home page
            return redirect(url_for('main.index'))
        else:
            # Invalid login message
            update_login_attempt(user.uuid if user else None, False)
            return render_template('auth/login.html', title="Login", error="foo", form=form)

    return render_template('auth/login.html', title='Login', form=form)

#@auth.route('/forgot_password')
#def forgot_password():

#@auth.route('insert_password')
#def insert_password():




