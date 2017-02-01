import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql+psycopg2://' +
                                         os.environ['USER'] + ':' +
                                         os.environ['PASS'] +
                                         '@localhost/practice')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'practice'

    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(25), unique=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    id = db.Column(db.Integer, primary_key=True)

    def insert(submit_db):
        db.session.add(submit_db)
        db.session.commit()

    def __init__(self, username, password, email, first_name, last_name):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return ('<User(username=%s, password=%s, email=%s,' +
                'first_name=%s, last_name=%s)>') % (self.username,
                                                    self.password,
                                                    self.email,
                                                    self.first_name,
                                                    self.last_name)
