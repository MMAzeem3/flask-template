#! /usr/bin/env python3

from enum import unique
from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
import os
import csv
import secrets
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = secrets.token_hex()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UserInfo.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.view ='login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# create User Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(2000))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribtue')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name

# Create User Form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash_confirm', message='Passwords must match')])
    password_hash_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()     #query database - get all users with submitted email address - should be none
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, password=form.password_hash.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash = ''
    our_users = Users.query.order_by(Users.date_added)  # get all users
    return render_template('add_user.html', 
                           form=form,
                           name=name,
                           our_users=our_users)

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if user.verify_password(form.password.data):
                login_user(user)
                return redirect('/dashboard')
            else:
                # todo flash
                return 'wrong'
        else:
            return 'that email doesnt exist'
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    # todo flash
    return redirect(url_for('login'))

@app.route("/")
@login_required
def index():
    return render_template('index.html')
# Registered participants

ppl = []
if os.path.isfile("registrants.csv"):
    ppl = open("registrants.csv").read().splitlines()

@app.route("/register", methods=["POST"])
@login_required
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
@login_required
def registrants():
    return render_template("registrants.html", ppl=ppl)

if __name__=='__main__':
    app.run(debug=True)