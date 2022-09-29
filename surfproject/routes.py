from flask import render_template, request, redirect, url_for
from surfproject import app, db
from surfproject.models import Review, Camp
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "PUSH"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
    return render_template("register.html")


@app.route("/camps")
def camps():
    camps = list(Camp.query.order_by(Camp.camp_name).all())
    return render_template("camps.html", camps=camps)


@app.route("/get_reviews")
def get_reviews():
    reviews = mongo.db.tasks.find()
    return render_template("reviews.html", tasks=tasks)


@app.route("/reviews/<int:camp_id>", methods=["GET"])
def reviews(camp_id):
    reviews = list(Review.query.all())
    return render_template("reviews.html", reviews=reviews, camp_id=camp_id)


@app.route("/new_camp", methods=["GET", "POST"])
def new_camp():
    if request.method == "POST":
        camp = Camp(camp_name=request.form.get("camp_name"))
        db.session.add(camp)
        db.session.commit()
        return redirect(url_for("camps"))
    return render_template("new_camp.html")


@app.route("/new_review", methods=["GET", "POST"])
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
        return redirect(url_for("camps"))
    return render_template("new_review.html", camps=camps)


@app.route("/edit_review/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    camps = list(Camp.query.order_by(Camp.camp_name).all())
    if request.method == "POST":
        review.review_name = request.form.get("review_name"),
        review.review_text = request.form.get("review_text"),
        review.camp_id = request.form.get("camp_id")
        db.session.commit()
        return redirect(url_for("camps"))
    return render_template("edit_review.html", review=review, camps=camps)


@app.route("/delete_review/<int:review_id>")
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for("home"))
