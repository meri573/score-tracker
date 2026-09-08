from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit_score")
def submit_score():
    return render_template("submit_score.html")

@app.route("/result", methods=["POST"])
def result():
    game = request.form["game"]
    extras = request.form.getlist("extra")
    description = request.form["description"]
    return render_template("result.html", game=game, extras=extras, description=description)