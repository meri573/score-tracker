import sqlite3
from flask import Flask
from flask import redirect,render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import result_handler

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "ERROR: passwords don't match"
    password_hash = generate_password_hash(password1)

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
        session["username"] = username
        sql = "SELECT id FROM users WHERE username = ?"
        session["user_id"] = db.query(sql, [username])[0][0]
        print(session["user_id"])

        return redirect("/")
    else:
        return "ERROR: wrong username or password"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/results")
def results():
    results = result_handler.get_results()
    return render_template("results.html",results=results)

@app.route("/result/<int:result_id>")
def result(result_id):
    print(result_id)
    result = result_handler.get_result(result_id)
    print(result)
    for thing in result:
        print(thing[0])

    return render_template("result.html", result=result)




@app.route("/submit_score")
def submit_score():
    return render_template("submit_score.html")

@app.route("/submission", methods=["POST"])
def submission():
    game = request.form["game"]
    time = request.form["time"]
    grade = request.form["grade"]
    score = request.form["score"]
    big_mode = 0
    twentyg_mode = 0 
    extras = request.form.getlist("extra")
    description = request.form["description"]
    user_id = session["user_id"]

    for extra in extras:
        if extra == "twentyg_mode":
            twentyg_mode = 1
        if extra == "big_mode":
            big_mode = 1

    sql = "INSERT INTO results (game, result_time, score, grade, big_mode, twentyg_mode, result_description, submitted_at, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), ?)"
    db.execute(sql, [game, time, grade, score, big_mode, twentyg_mode, description, user_id])

    print(game, time, grade, score, big_mode, twentyg_mode, description, user_id)
    return render_template("submission.html", game=game, extras=extras, description=description)