import psycopg2
import hashlib
import uuid
import os
from flask import Flask, render_template, request
from flask_api import status
from wtforms import Form, StringField, PasswordField, validators

app = Flask(__name__)
conn_string = ("host=localhost dbname=practice user=" +
               os.environ['USER'] + " password=" + os.environ['PASS'])


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [validators.Length(min=6, max=20)])

def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


# route for index
@app.route("/", methods=['GET', 'POST'])
def index():
    form = LoginForm(request.form)
    try:
        if request.method == 'POST' and form.validate():
            username = request.form['username']
            password = hash_password(request.form['password'])

            conn = psycopg2.connect(conn_string)
            cursor = conn.cursor()
            print("Connected!")

            cursor.execute(
                """INSERT INTO practice (username, password)
                    VALUES (%s, %s);""",
                (username, password))
            conn.commit()
            return render_template("index.html"), status.HTTP_201_CREATED
    except Exception:
        return render_template("index.html",
                               warning="Username " + username +
                               " is already taken!"), status.HTTP_409_CONFLICT
    return render_template("index.html", form=form)


# route for db on GET or POST testing
@app.route("/db", methods=['GET', 'POST'])
def to_db():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print("Connected!")

    cursor.execute(
        """INSERT INTO practice (username, password)
            VALUES (%s, %s);""",
        ('one', 'two'))
    conn.commit()

    return '', status.HTTP_201_CREATED


# route for each profile page
@app.route("/profile/<username>", methods=['GET', 'POST'])
def profile(username):
    conn = psycopg2.connect(conn_string)
    return render_template("profile.html", username=username)


if __name__ == "__main__":
    app.run(debug=True)
