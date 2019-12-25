import functools
import psycopg2

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import psycopg2
from flaskr.db import connect

bp = Blueprint('auth', __name__, url_prefix='/auth')

#register page logic
@bp.route('/register', methods=('GET', 'POST'))
def register():
    #grab passed values from POST
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #connect to DB
        conn = connect()
        cur = conn.cursor()
        error = None

        #validate UN and PW were entered or and user isn't already registered
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            cur.execute(
                'SELECT id FROM users WHERE username = (%s)', (username,))
            result = cur.fetchone()
            if result is not None:
                error = 'User {} is already registered.'.format(username)

        # if passed above checks, register user and redirect to login page
        if error is None:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, generate_password_hash(password,method='pbkdf2:sha256:1000000')))

            conn.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

#login page logic
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #connect to DB
        conn = connect()
        cur = conn.cursor()

        # checks DB if UN exists
        error = None
        cur.execute(
            'SELECT id, username, password FROM users WHERE username = (%s)', (username,))
        user = cur.fetchone()

        # checks UN is correct and PW is correct
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        # if passed above checks, log in, set session with user data and go to home page
        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

#runs before view is rendered - checks if session exists and if so, sets username. creates persistency
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        conn = connect()
        cur = conn.cursor()

        #if session exists, grab user data from DB and store in g.user (multi-threaded session agnostic object)
        cur.execute(
            'SELECT * FROM users WHERE id = (%s)', (user_id,))
        g.user = cur.fetchone()

# clears session in case of logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# decorator that re-directs to home if the session is not set - to be used on pages that require login to be viewed
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
