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
from flask_socketio import SocketIO, emit, send

from db import User, Chat

app = Flask(__name__)
app.secret_key = os.environ['KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)


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

        try:
            hashed_password = User.query_pwd(username=username).password
        except AttributeError:
            warn = 'Username or password was incorrect!'
            return (render_template('index.html', form=form, warn=warn),
                    status.HTTP_406_NOT_ACCEPTABLE)

        login = check_password(hashed_password, user_password)

        if login is False:
            warn = 'Username or password was incorrect!'
            return (render_template('index.html', form=form, warn=warn),
                    status.HTTP_406_NOT_ACCEPTABLE)
        elif login is True:
            session['username'] = request.form['username']
            print('%s: you are logged in!' % login)
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
            user_exept = 'entries_username_key'
            email_exept = 'entries_email_key'
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
            else:
                warn = 'Database error!'
                print(str_e)
                return (render_template('register.html', form=form, warn=warn),
                        status.HTTP_500_INTERNAL_SERVER_ERROR)
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


# route for chat
@app.route('/chat', methods=['GET'])
def chat():
    if request.method == 'GET':
        timestamp_list = []
        history = Chat.query.all()
        for entries in history:
            x = entries.msg_timestamp
            timestamp_list.append(x)
        print('Printing \'timestamp_list\': %s' % timestamp_list)
    return render_template('chat.html', messages=history)


@socketio.on('message')
def test_message(msg):
    print(msg)
    try:
        current_user = session['username']
    except KeyError:
        current_user = 'anonymous'

    messages = msg
    submit_db = Chat(current_user, messages)
    Chat.insert(submit_db)
    send(msg, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
