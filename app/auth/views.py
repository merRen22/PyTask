from flask import render_template, url_for, flash, redirect
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth

from app.forms import LoginForm
from app.firestore_service import get_user, user_put
from app.models import UserModel, UserData


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_official = user_doc.to_dict()['password']

            if check_password_hash(password_official, password):
                user_data = UserData(username, generate_password_hash(password))
                user = UserModel(user_data)

                login_user(user)

                flash('Welcome again')

                redirect(url_for('hello'))
            else:
                flash('Information does not make sense')
        else:
            flash('User is not registered')

        return redirect(url_for('index'))

    return render_template('login.html', **context)


@auth.route('signup', methods=['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(
                username=username,
                password=password_hash
            )
            user_put(user_data)

            user = UserModel(user_data)

            login_user(user)

            flash('Welcome')

            return redirect(url_for('hello'))
        else:
            flash('User is already registered')

    return render_template('signup.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Bye 👋 see u soon')

    return redirect(url_for('auth.login'))
