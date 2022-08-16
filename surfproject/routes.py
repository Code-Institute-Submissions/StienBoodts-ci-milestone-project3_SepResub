from flask import render_template, request, redirect, url_for
from surfproject import app, db
from surfproject.models import Review, Camps

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/camps")
def camps():
    camps = list(Camps.query.order_by(Camps.camp_name).all())
    return render_template("camps.html")

@app.route("/new_review", methods=["GET","POST"])
def new_review():
    if request.method == "POST":
        review = Review(
            camp_name=request.form.get("camp_name"),
            camp_country=request.form.get("camp_country"),
            review_text=request.form.get("review_text"),
        )
        db.session.add(review)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_review.html")