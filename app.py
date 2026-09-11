import sqlite3
from flask import Flask
from flask import render_template, request
from werkzeug.security import generate_password_hash
import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template(register.html)

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "ERROR: passwords don't match"
    password_hash = generate_password_hash

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?,?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "ERROR: username already exists"

    return "Account created"

@app.route("/submit_score")
def submit_score():
    return render_template("submit_score.html")

@app.route("/result", methods=["POST"])
def result():
    game = request.form["game"]
    extras = request.form.getlist("extra")
    description = request.form["description"]
    return render_template("result.html", game=game, extras=extras, description=description)