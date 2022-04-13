#! /usr/bin/env python3

from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def homepage():
    name = request.args.get("name", "world")
    return render_template('simple.html', name=name)


@app.route("/<name>")
def hello(name):
    return f"<p>Hello {escape(name)}</p>"


app.run(debug=True)