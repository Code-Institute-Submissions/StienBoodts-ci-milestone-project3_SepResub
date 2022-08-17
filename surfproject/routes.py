from flask import render_template, request, redirect, url_for
from surfproject import app, db
from surfproject.models import Review, Camps

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/camps")
def camps():
    camps = list(Camps.query.order_by(Camps.camp_name).all())
    return render_template("camps.html", camps=camps)


@app.route("/new_camp", methods=["GET", "POST"])
def new_camp():
    if request.method == "POST":
        camp = Camps(camp_name=request.form.get("camp_name"))
        db.session.add(camp)
        db.session.commit()
        return redirect(url_for("camps"))
    return render_template("new_camp.html")


@app.route("/new_review", methods=["GET","POST"])
def new_review():
    camps = list(Camps.query.order_by(Camps.camp_name).all())
    if request.method == "POST":
        review = Review(
            review_name=request.form.get("review_name"),
            review_text=request.form.get("review_text"),
            camp_id=request.form.get("camp_id")
        )
        db.session.add(review)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_review.html", camps=camps)