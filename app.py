import hashlib
import uuid
import os

from flask import Flask, render_template, request, session, redirect, \
    url_for, flash
from flask_api import status
from wtforms import Form, StringField, PasswordField, validators
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from db import User

app = Flask(__name__)
app.secret_key = os.environ['KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class LoginForm(Form):
    username = StringField('Username',
                           [validators.Length(min=2, max=20)])
    password = PasswordField('New Password',
                             [validators.Length(min=8, max=20)])


class RegistrationForm(Form):
    username = StringField('Username',
                           [validators.Length(min=2, max=20)])
    password = PasswordField('New Password',
                             [validators.Length(min=8, max=20)])
    email = StringField('Email Address',
                        [validators.Length(min=6, max=35)])
    first_name = StringField('First Name',
                             [validators.Length(min=2, max=35)])
    last_name = StringField('Last Name',
                            [validators.Length(min=2, max=35)])


def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() +
                          password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() +
                                      user_password.encode()).hexdigest()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if any(session) is False:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# route for index
@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form['username']
        user_password = request.form['password']
        hashed_password = User.query.filter_by(username=username).first()
        login = check_password(hashed_password.password, user_password)
        print('%s: you are logged in!' % login)

        if login is True:
            session['username'] = request.form['username']
            print('Session active!')
            print(session)
            flash('You are logged in!')
            return redirect(url_for('profile', username=username))
        return render_template('index.html',
                               form=form), status.HTTP_201_CREATED
    return render_template('index.html', form=form)


# route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            username = request.form['username']
            password = hash_password(request.form['password'])
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']

            print(username + '\n' + password + '\n' + email + '\n' +
                  first_name + '\n' + last_name)

            submit_db = User(username, password, email, first_name, last_name)
            User.insert(submit_db)
            return render_template('index.html',
                                   form=form), status.HTTP_201_CREATED
        except exc.SQLAlchemyError as e:
            str_e = str(e)
            print(str_e)
            user_exept = 'practice_username_key'
            email_exept = 'practice_email_key'
            if user_exept in str_e:
                warn = 'Username \'' + username + '\' is already taken!'
                User.rollback()
                return render_template('register.html', form=form,
                                       warn=warn), status.HTTP_409_CONFLICT
            elif email_exept in str_e:
                warn = 'Email address \'' + email + '\' is already taken!'
                User.rollback()
                return render_template('register.html', form=form,
                                       warn=warn), status.HTTP_409_CONFLICT
    return render_template('register.html', form=form)


# route for each profile page
@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    print('Printing session[\'username\']: %s' % session['username'])
    if username != session['username']:
        return redirect(url_for('index'))

    if request.method == 'GET':
        load_profile = User.query.filter_by(username=session['username']
                                            ).first()
        user = load_profile.username
        email = load_profile.email
        first_name = load_profile.first_name
        last_name = load_profile.last_name
        return render_template('profile.html', username=username, user=user,
                               email=email, first_name=first_name,
                               last_name=last_name)
    if request.method == 'POST':
        return redirect(url_for('logout'))
    return render_template('profile.html', username=username)


# logout route for button
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.pop('username', None)
        print('Logged out!')
        return redirect(url_for('index'))

    session.pop('username', None)
    print('Logged out!')
    return redirect(url_for('index'))


# route for testing only
@app.route('/test')
def test():
    print('Current session: %s' % session)
    if any(session) is False:
        print('Empty session!')

    from_db = User.query.all()
    print(from_db)
    return 'Test page!', status.HTTP_200_OK

if __name__ == '__main__':
    app.run(debug=True)
