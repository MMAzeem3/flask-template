#! /usr/bin/env python3

from flask import Flask, render_template, request, redirect
from markupsafe import escape
import os
import csv

app = Flask(__name__)

# Registered participants
ppl = []
if os.path.isfile("registrants.csv"):
    ppl = open("registrants.csv").read().splitlines()

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/register", methods=["POST"])
def register():
    # get values with http request
    name = request.form.get("name")
    age = request.form.get("age")
    state = request.form.get("state")
    if not name or not age or not state:
        # check for valid input
        return render_template('invalid.html')
    with open("registrants.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow([name, age, state])
    ppl.append(open("registrants.csv").readlines()[-1])
    return render_template("register.html", person=ppl[-1])

@app.route("/registrants")
def registrants():
    return render_template("registrants.html", ppl=ppl)