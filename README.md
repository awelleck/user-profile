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

* Source username and password for database
* `python app.py`
* `curl -X POST -d "{ username: '', password: '' }" localhost:5000/db`

or
* Use http://127.0.0.1:5000/ in browser

To dump/restore PostgreSQL database

* `pg_dump dbname > outfile`
* `psql dbname < infile`
