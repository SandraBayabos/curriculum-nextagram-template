from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from instagram_web.util.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/signin', methods=['GET'])
def show():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def sign_in():
    email = request.form.get('email')
    password_to_check = request.form.get('password')

    user = User.get_or_none(User.email == email)

    if not user:
        flash('Invalid Email provided, please check and try again!')
        return render_template('sessions/new.html')

    hashed_password = user.password

    if not check_password_hash(hashed_password, password_to_check):
        flash('Incorrect password! Please try again!')
        return render_template('sessions/new.html')

    # session['user_id'] = user.id
    # remove session['user_id'] = user.id & insert login_user(user) from flask-login to sign in
    login_user(user)
    flash(f'Welcome back {user.username}. You are logged in.')
    return redirect(url_for('home'))


@sessions_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('home'))


# Google OAuth
@sessions_blueprint.route('/google_login/authorize', methods=['GET'])
def authorize():
    token = oauth.google.authorize_access_token()

    if token:
        email = oauth.google.get(
            'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
        user = User.get_or_none(User.email == email)

        if not user:
            flash('No user registered with this account.')
            return redirect(url_for('sessions.show'))

    flash(f'Welcome back {user.username}')
    return redirect(url_for('users.edit', id=user.id))

    return redirect(url_for('sessions.google_login'))


@sessions_blueprint.route('/google_login', methods=['GET'])
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
