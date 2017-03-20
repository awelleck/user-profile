import unittest
from utils import db
from models import User
from flask import Flask
from flask_testing import TestCase


username = 'one'
password = 'two'
email = 'three@four.com'
first_name = 'five'
last_name = 'six'

class MyTest(TestCase):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True

    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        db.app = app
        return app

    def setUp(self):
        db.session.remove()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_insert(self):
        user = User(username, password, email, first_name, last_name)

        db.session.add(user)
        db.session.commit()

        actual = User.query.filter_by(username=username).first()

        self.assertEqual(username, actual.username)
        self.assertEqual(password, actual.password)
        self.assertEqual(email, actual.email)
        self.assertEqual(first_name, actual.first_name)
        self.assertEqual(last_name, actual.last_name)


if __name__ == '__main__':
    unittest.main()
