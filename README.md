# user-profile

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
* `python app.py`

To test
* `curl -X POST -d "{ first_name: '', last_name: '' }" localhost:5000/db`
