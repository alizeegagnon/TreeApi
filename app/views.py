from app import app 
import os


@app.route("/")
def index():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)

@app.route("/about")
def about():
    return "A Flask test"
