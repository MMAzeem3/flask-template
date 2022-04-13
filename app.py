#! /usr/bin/env python3

from flask import Flask, render_template, request, redirect
from markupsafe import escape
import os
import smtplib

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/register", methods=["POST"])
def register():
    # get values with http request
    name = request.form.get("name")
    age = request.form.get("age")
    email = request.form.get("email")
    state = request.form.get("state")
    if not name or not age or not state or not email:
        # check for valid input
        return render_template('invalid.html')
    message = "You are registered"
    server = smtplib.SMTP("smtp.gmail.com", 587)     #domain of smtp email
    server.starttls()
    server.login("pythontesting1029@gmail.com", os.getenv("PASSWORD"))
    server.sendmail("pythontesting1029@gmail.com", email, message)
    return redirect("/registrants")

@app.route("/registrants")
def registrants():
    return render_template("registrants.html")