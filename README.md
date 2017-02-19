# user-profile
[![Build Status](https://travis-ci.org/awelleck/user-profile.svg?branch=master)](https://travis-ci.org/awelleck/user-profile)

Building a user profile system with authentication. Using this as a place for notes as I go along, hopefully most makes it in the final README or automation script.

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
