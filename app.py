from flask import Flask
app = Flask(__name__)

# decorator for index
@app.route("/")
def index():
    return "Index"

@app.route("/<username>")
def profile(username):
	return "Hello %s" % username

if __name__ == "__main__":
    app.run(debug=True)
