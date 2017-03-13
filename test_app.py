import sqlite3
import unittest
import sqlalchemy
from db import User, Chat
from flask import Flask
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy

class MyTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        app = Flask(__name__)
        #app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        db = SQLAlchemy(app)
        print("creating app")
        self.db = db
        return app

    def setUp(self):
        #app = create_app()
        print("Setting up DB and stuff")
        self.db.create_all()
        self.db.session.commit()
        print(self.db.reflect())

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

class SomeTest(MyTest):

    def test_something(self):
        username = 'one'
        password = 'two'
        email = 'three@four.com'
        first_name = 'five'
        last_name = 'six'

        user = User(username, password, email, first_name, last_name)

        self.db.session.add(user)
        self.db.session.commit()

        # this works
        assert user in self.db.session

        #response = self.client.get("/")

        # this raises an AssertionError
        #assert user in db.session

if __name__ == '__main__':
    unittest.main()
