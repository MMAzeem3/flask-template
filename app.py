#! /usr/bin/env python3

from enum import unique
from flask import Flask, render_template, request, redirect
from markupsafe import escape
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
import csv
import secrets
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = secrets.token_hex()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

# Registered participants
ppl = []
if os.path.isfile("registrants.csv"):
    ppl = open("registrants.csv").read().splitlines()

# create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Name %r>' % self.name

# Create User Form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()     #query database - get all users with submitted email address - should be none
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
    our_users = Users.query.order_by(Users.date_added)  # get all users
    return render_template('add_user.html', 
                           form=form,
                           name=name,
                           our_users=our_users)

@app.route("/")
def index():
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

if __name__=='__main__':
    app.run(debug=True)