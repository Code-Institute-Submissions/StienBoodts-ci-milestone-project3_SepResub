from flask import render_template, request, redirect, url_for
from surfproject import app, db
from surfproject.models import Review, Camp

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/camps")
def camps():
    camps = list(Camp.query.order_by(Camp.camp_name).all())
    return render_template("camps.html", camps=camps)


@app.route("/reviews/<int:camp_id>", methods=["GET"])
def reviews(camp_id):
    review = Review.query.get_or_404(camp_id)
    return render_template("reviews.html", review=review)

@app.route("/new_camp", methods=["GET", "POST"])
def new_camp():
    if request.method == "POST":
        camp = Camp(camp_name=request.form.get("camp_name"))
        db.session.add(camp)
        db.session.commit()
        return redirect(url_for("camps"))
    return render_template("new_camp.html")


@app.route("/new_review", methods=["GET","POST"])
def new_review():
    camps = list(Camp.query.order_by(Camp.camp_name).all())
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


@app.route("/edit_review/<int:review_id>", methods=["GET","POST"])
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    camps = list(Camps.query.order_by(Camps.camp_name).all())
    if request.method == "POST":
        review.review_name = request.form.get("review_name"),
        review.review_text = request.form.get("review_text"),
        review.camp_id = request.form.get("camp_id")
        db.session.commit()
    return render_template("edit_review.html", review=review, camps=camps)