import hashlib
import uuid
import os

from flask import Flask, render_template, request, session, redirect, \
    url_for, flash
from flask_api import status
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_socketio import SocketIO, Namespace, send, emit, disconnect
from models import User, Chat
from validate import LoginForm, RegistrationForm, ProfileForm
from chat import MyNamespace
from utils import db

app = Flask(__name__)
app.secret_key = os.environ['KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql+psycopg2://' +
                                         os.environ['USER'] + ':' +
                                         os.environ['PASS'] +
                                         '@localhost/practice')
db.init_app(app)
db.app = app
socketio = SocketIO(app)
socketio.on_namespace(MyNamespace('/chat'))


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
            return redirect(url_for('login', next=request.url))
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
    form = ProfileForm(request.form)
    print('Printing session[\'username\']: %s' % session['username'])

    if username != session['username']:
        return redirect(url_for('index'))

    if request.method == 'POST':
        load_profile = User.query.filter_by(username=session['username']
                                            ).first()
        user = load_profile.username
        email = load_profile.email
        first_name = load_profile.first_name
        last_name = load_profile.last_name
        change_first_name = request.form['change_first_name']
        print(change_first_name)
        User.update(first_name, change_first_name)
        return render_template('profile.html',
                               form=form, username=username, user=user,
                               email=email, first_name=first_name,
                               last_name=last_name), status.HTTP_201_CREATED

    load_profile = User.query.filter_by(username=session['username']
                                        ).first()
    user = load_profile.username
    email = load_profile.email
    first_name = load_profile.first_name
    last_name = load_profile.last_name

    return render_template('profile.html', form=form, username=username,
                           user=user, email=email, first_name=first_name,
                           last_name=last_name)


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


# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        user_password = request.form['password']

        try:
            hashed_password = User.query_pwd(username=username).password
        except AttributeError:
            warn = 'Username or password was incorrect!'
            return (render_template('login.html', form=form, warn=warn),
                    status.HTTP_406_NOT_ACCEPTABLE)

        login = check_password(hashed_password, user_password)

        if login is False:
            warn = 'Username or password was incorrect!'
            return (render_template('login.html', form=form, warn=warn),
                    status.HTTP_406_NOT_ACCEPTABLE)
        elif login is True:
            session['username'] = request.form['username']
            return redirect(url_for('profile', username=username))

    return render_template('login.html', form=form)


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
@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'GET':
        current_user = session['username']
        history_list = []
        history = Chat.query.all()
        for entries in history:
            history_list.append((entries.username, entries.messages,
                                 entries.msg_timestamp))
        return render_template('chat.html', history=history_list,
                               current_user=current_user)


if __name__ == '__main__':
    socketio.run(app, debug=True)
