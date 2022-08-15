from flask import render_template
from surfproject import app, db
from surfproject.models import User, Review, Countries, Camps

@app.route("/")
def home():
    return render_template("camps.html")