"""
https://linuxize.com/post/how-to-install-flask-on-ubuntu-18-04/
"""

from flask import Flask

app = Flask(__name__)

from app import views

"""
@app.route("/start/move", methods=["POST"])
def make_move():
    return "Done"

"""