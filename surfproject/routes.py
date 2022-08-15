from flask import render_template
from surfproject import app, db
from surfproject.models import User, Review, Countries, Camps

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/camps")
def camps():
    return render_template("camps.html")

@app.route("/countries")
def countries():
    return render_template("countries.html")

@app.route("/new_review")
def new_review():
    return render_template("new_review.html")