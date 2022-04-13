#! /usr/bin/env python3

from flask import Flask, render_template, request, redirect
from markupsafe import escape

app = Flask(__name__)

# Registered participants
ppl = []

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/register", methods=["POST"])
def register():
    # get values with http request
    name = request.form.get("name")
    age = request.form.get("age")
    state = request.form.get("state")
    print(name)
    print(age)
    print(state)
    if not name or not age or not state:
        # check for valid input
        return render_template('invalid.html')
    ppl.append(f"{name}, {age} from {state}")
    return redirect("/registrants")

@app.route("/registrants")
def registrants():
    return render_template("registrants.html", ppl=ppl)