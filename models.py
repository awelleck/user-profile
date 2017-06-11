import os
from datetime import datetime
from flask import Flask, request
from utils import db


class User(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(25), unique=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))

    def query_pwd(username):
        db_entry = User.query.filter_by(username=username).first()
        return db_entry

    def insert(submit_db):
        db.session.add(submit_db)
        db.session.commit()

    def update(username, email, first_name, last_name):
        db_entry = User.query.filter_by(username=username).first()
        db_entry.email = email
        db_entry.first_name = first_name
        db_entry.last_name = last_name
        db.session.add(db_entry)
        db.session.commit()
        return True

    def delete(username):
        db.session.delete(username)
        db.session.commit()

    def rollback():
        db.session.rollback()

    def __init__(self, username, password, email, first_name, last_name):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return ('<User(username=%s, password=%s, email=%s, ' +
                'first_name=%s, last_name=%s)>') % (self.username,
                                                    self.password,
                                                    self.email,
                                                    self.first_name,
                                                    self.last_name)


class Chat(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    messages = db.Column(db.String(500))
    msg_timestamp = db.Column(db.DateTime)

    def insert(submit_db):
        db.session.add(submit_db)
        db.session.commit()

    def __init__(self, username, messages, msg_timestamp=None):
        self.username = username
        self.messages = messages
        if msg_timestamp is None:
            msg_timestamp = datetime.utcnow()
        self.msg_timestamp = msg_timestamp

    def __repr__(self):
        return (('<Chat(username=%s, messages=%s, timestamp=%s)>') %
                (self.username, self.messages, self.msg_timestamp))
