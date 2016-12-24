import psycopg2
from flask import Flask, render_template
from flask_api import status

app = Flask(__name__)
conn_string = "host='localhost' dbname='practice' user='' password=''"

# decorator for index
@app.route("/", methods=('GET','POST'))
def index():
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	print ("Connected!\n")
	return render_template("index.html")

@app.route("/db", methods=('GET','POST'))
def to_db():
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	print ("Connected!\n")
	cursor.execute(
    	"""INSERT INTO practice (first_name, last_name)
        	VALUES (%s, %s);""",
    	('one', 'two'))
	conn.commit()
	return '', status.HTTP_201_CREATED

# decorator for each profile page
@app.route("/profile/<username>", methods=('GET','POST'))
def profile(username):
	conn = psycopg2.connect(conn_string)
	return render_template("profile.html", username=username)

if __name__ == "__main__":
    app.run(debug=True)
