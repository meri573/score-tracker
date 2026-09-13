import sqlite3
from flask import Flask
from flask import redirect,render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
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

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql,[username])[0][0]

    if check_password_hash(password_hash, password):
        session[username] = username
        return redirect("/")

@app.route("/submit_score")
def submit_score():
    return render_template("submit_score.html")

@app.route("/result", methods=["POST"])
def result():
    game = request.form["game"]
    time = 
    grade = 
    score = 
    big_mode = 0
    20g_mode = 0 
    extras = request.form.getlist("extra")
    description = request.form["description"]
    user_id =

    for extra in extras:
        if extra = "20g_mode":
            20g_mode = 1
        if extra = "big_mode": 
            big_mode = 1

    sql = "INSERT INTO results (game, time, grade, score, big_mode, 20g_mode, description, submitted_at, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, datetime("now"), user_id)"

    return render_template("result.html", game=game, extras=extras, description=description)