# user-profile
[![Build Status](https://travis-ci.org/awelleck/user-profile.svg?branch=master)](https://travis-ci.org/awelleck/user-profile)

User profile system with authentication:

* Web framework: [Flask](http://flask.pocoo.org/)
* Backend framework: [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/) using [Psycopg2](http://initd.org/psycopg/docs/) driver to connect to [PostgreSQL](https://www.postgresql.org/) relational database
* Form validation by [WTForms](http://wtforms.readthedocs.io/en/latest/)
* Front-end framwork by [Material Design Lite](https://getmdl.io/)
* Client/server communication for chat leverages [Flask-Socket IO](https://flask-socketio.readthedocs.io/en/latest/) and [Eventlet](http://eventlet.net/)

<div><img src="https://github.com/awelleck/user-profile/blob/master/static/index.png" width="300">
<img src="https://github.com/awelleck/user-profile/blob/master/static/chat.png" width="310"></div>

Using [Homebrew](http://brew.sh/) for package manager

* `brew update`
* `brew doctor`
* `brew install python3`
* `brew install postgresql`

Setting up virtualenv to use Python 3

* `virtualenv ENV`
* `source ENV/bin/activate`
* `virtualenv -p python3 env`
* `pip install -r requirements.txt`

To test

* Source username and password for database as well as the key for Python Flask sessions
* `python app.py`
* To run tests: `python test_app.py`
* Tests are also automatically run with each build by TravisCI

or

* Use http://127.0.0.1:5000/ in browser

To dump/restore PostgreSQL database

* `pg_dump dbname > outfile`
* `psql dbname < infile`

To create DB tables

* `\i schema.sql` from psql prompt

Granting permissions for DB for both tables

* `GRANT ALL PRIVILEGES ON TABLE entries TO db_user;`
* `GRANT USAGE ON SEQUENCE entries_id_seq TO db_user;`
* `GRANT ALL PRIVILEGES ON TABLE chat TO db_user;`
* `GRANT USAGE ON SEQUENCE chat_id_seq TO db_user;`
