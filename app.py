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
import comments

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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
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

@app.route("/user/<int:user_id>")
def user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    results = users.get_results(user_id)
    user_comments = comments.get_user_comments(user_id)
    if not user_comments:
        user_comments = []
    return render_template("user.html", user=user, results=results, user_comments=user_comments)


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
    classes = result_handler.get_classes(result_id)
    result_comments = comments.get_comments(result_id)
    if not result_comments:
        result_comments = []

    return render_template("result.html", result=result, result_comments=result_comments, classes=classes)

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

@app.route("/new_comment", methods=["POST"])
def new_comment():
    require_login()
    check_csrf()
    
    content = request.form["content"]
    if len(content) > 200:
        abort(403)    
    result_id = int(request.form["result_id"])
    user_id = session["user_id"]

    comments.add_comment(result_id, content, user_id)
    return redirect("/result/" + str(result_id))

@app.route("/edit_comment/<int:comment_id>")
def edit_comment(comment_id):
    require_login
    comment = comments.get_comment(comment_id)
    if not comment:
        abort(404)
    if comment["user_id"] != session["user_id"]:
        abort(403)

    return render_template("edit_comment.html", comment=comment)

@app.route("/update_comment", methods=["POST"])
def update_comment():
    require_login()
    check_csrf()

    comment_id = int(request.form["comment_id"])
    comment = comments.get_comment(comment_id)
    if not result:
        abort(404)
    if comment["user_id"] != session["user_id"]:
        abort(403)

    content = request.form["content"]
    if not content or len(content) >200:
        abort(403)

    print(comment_id)
    print(content)
    comments.update_comment(comment_id, content)

    return redirect("/result/" + str(comment["result_id"]))


@app.route("/delete_comment/<int:comment_id>", methods=["GET", "POST"])
def delete_comment(comment_id):
    require_login()

    comment = comments.get_comment(comment_id)
    if not comment:
        abort(404)
    if comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete_comment.html", comment=comment)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            comments.delete_comment(comment_id)
            return redirect("/result/" + str(comment["result_id"]))


@app.route("/submit_score")
def submit_score():
    classes = result_handler.get_all_classes()
    return render_template("submit_score.html", classes=classes)

@app.route("/submission", methods=["POST"])
def submission():
    require_login()
    check_csrf()


    time = request.form["time"]
    score = request.form["score"]
    description = request.form["description"]
    user_id = session["user_id"]

    all_classes = result_handler.get_all_classes()

    print(request.form.getlist("extras"))

    classes = []
    temp_classes = [request.form["game"], request.form["grade"], request.form["rule"]]
    temp_classes.extend(request.form.getlist("extras"))
    for entry in temp_classes:
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))
        else:
            abort(403)

    print(classes)


    if not time or len(time) > 20:
        abort(403)
    if not score or len(score) > 20:
        abort(403)
    if description and len(description) >200:
        abort(403)

    result_handler.add_result(time, score, description, user_id, classes)

    return redirect("/results")