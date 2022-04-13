#! /usr/bin/env python3

from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")     #get values with http request
    age = request.form.get("age")
    state = request.form.get("state")
    print(name)
    print(age)
    print(state)
    if not name or not age or not state:
        return render_template('invalid.html')
    return render_template('register.html')
