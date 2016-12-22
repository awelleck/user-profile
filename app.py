from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/[practice]'
db = SQLAlchemy(app)

# decorator for index
@app.route("/")
def index():
    return render_template("index.html")

# decorator for each profile page
@app.route("/profile/<username>")
def profile(username):
	return render_template("profile.html", username=username)

@app.route("/db", method=['PUT'])
def to_db():
	print("PUT to db")

if __name__ == "__main__":
    app.run(debug=True)
