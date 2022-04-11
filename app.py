#! /usr/bin/env python3

from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route("/<name>")
def hello(name):
    return f"<p>Hello {escape(name)}</p>"

@app.route("/")
def homepage():
    return render_template('simple.html')

app.run(debug=True)