from flask import render_template, session, redirect, url_for
from . import auth
from .forms import RegistrationForm,LoginForm
from .helper import update_login_attempt
from ..models import Login
from ..extensions import db



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

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Login.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.uuid
            update_login_attempt(user.uuid, True) 
            # Redirect to the home page
            return redirect(url_for('main.index'))
        else:
            # Invalid login message
            update_login_attempt(user.uuid if user else None, False)
            return render_template('auth/login.html', title="Login", error="foo", form=form)

    return render_template('auth/login.html', title='Login', form=form)
