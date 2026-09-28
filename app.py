import sqlite3
import secrets
import re

from flask import Flask
from flask import redirect,render_template, request, session, abort
from werkzeug.security import generate_password_hash, check_password_hash

import db
import config
import result_handler
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


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
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "ERROR: username already exists"

    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user_id = users.check_login(username, password)
    if user_id:
        session["username"] = username
        session["user_id"] = user_id
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    else:
        return "ERROR: wrong username or password"

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/results")
def results():
    results = result_handler.get_results()
    return render_template("results.html",results=results)

@app.route("/result/<int:result_id>")
def result(result_id):
    result = result_handler.get_result(result_id)
    if not result:
        abort(404)

    return render_template("result.html", result=result)

@app.route("/delete_result/<int:result_id>", methods=["GET", "POST"])
def delete_result(result_id):
    require_login()

    result = result_handler.get_result(result_id)
    if not result:
        abort(404)
    if result["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete_result.html", result=result)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            result_handler.delete_result(result_id)
            return redirect("/")

@app.route("/edit_result/<int:result_id>")
def edit_result(result_id):
    require_login()
    result = result_handler.get_result(result_id)
    if not result:
        abort(404)
    if result["user_id"] != session["user_id"]:
        abort(403)
    
    return render_template("edit_result.html", result=result)

@app.route("/update_result", methods=["POST"])
def update_result():
    require_login()
    check_csrf()

    result_id = request.form["result_id"]
    result = result_handler.get_result(result_id)
    if not result:
        abort(404)
    if result["user_id"] != session["user_id"]:
        abort(403)

    description = request.form["description"]
    if not description or len(description) >200:
        abort(403)

    result_handler.update_result(result_id, description)

    return redirect("/results")

@app.route("/search_results")
def search_results():
    query = request.args.get("query")
    if query:
        results = result_handler.search_results(query)
    else:
        query = ""
        results = []
    return render_template("search_results.html", query=query, results=results)

@app.route("/submit_score")
def submit_score():
    return render_template("submit_score.html")

@app.route("/submission", methods=["POST"])
def submission():
    require_login()
    check_csrf

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

    if not re.search("Tetris: The Grand Master 1|2|3", game):
        abort(403)
    if not time:
        abort(403)
    if not grade:
        abort(403)
    if not score:
        abort(403)
    if description and len(description) >200:
        abort(403)

    sql = "INSERT INTO results (game, time, score, grade, big_mode, twentyg_mode, description, submitted_at, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), ?)"
    db.execute(sql, [game, time, score, grade, big_mode, twentyg_mode, description, user_id])

    return redirect("/results")