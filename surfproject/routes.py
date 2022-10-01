from flask import flash, render_template, request, redirect, session, url_for
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from surfproject import app, db, mongo
from surfproject.models import Camp, Users


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = Users.query.filter(Users.user_name == \
                                           request.form.get("username").lower()).all()
        
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        
        user = Users(
            user_name=request.form.get("username").lower(),
            password=generate_password_hash(request.form.get("password"))
        )
        
        db.session.add(user)
        db.session.commit()

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = Users.query.filter(Users.user_name == \
                                           request.form.get("username").lower()).all()

        if existing_user:
            print(request.form.get("username"))
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user[0].password, request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    if "user" in session:
        return render_template("profile.html", username=session["user"])

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/camps")
def camps():
    camps = list(Camp.query.order_by(Camp.camp_name).all())
    return render_template("camps.html", camps=camps)


@app.route("/get_reviews")
def get_reviews():
    reviews = list(mongo.db.reviews.find())
    return render_template("reviews.html", reviews=reviews)


@app.route("/reviews/<camp_id>", methods=["GET", "POST"])
def reviews(camp_id):
    reviews = list(mongo.db.reviews.find())
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
    if "user" not in session:
        flash("You need to be logged in to add a review")
        return redirect(url_for("get_reviews"))
    
    if request.method == "POST":
        review = {
            "review_name": request.form.get("review_name"),
            "review_text": request.form.get("review_text"),
            "camp_id": request.form.get("camp_id"),
            "created_by": session["user"]
        }
        mongo.db.reviews.insert_one(review)
        flash("Review Successfully Added")
        return redirect(url_for("get_reviews"))
    
    camps = list(Camp.query.order_by(Camp.camp_name).all())
    return render_template("new_review.html", camps=camps)


@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})

    if "user" not in session or session["user"] != review["created_by"]:
        flash("You can only edit your own reviews!")
        return redirect(url_for("get_reviews"))

    if request.method == "POST":
        submit = {
        "review_name": request.form.get("review_name"),
        "review_text": request.form.get("review_text"),
        "camp_id": request.form.get("camp_id"),
        "created_by": session["user"]
        }
        mongo.db.reviews.update({"_id": ObjectId(review_id)}, submit)
        flash("Review Successfully Updated")


    camps = list(Camp.query.order_by(Camp.camp_name).all())
    return render_template("edit_review.html", review=review, camps=camps)


@app.route("/delete_review/<review_id>")
def delete_review(review_id):

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})

    if "user" not in session or session["user"] != review["created_by"]:
        flash("You can only delete your own reviews!")
        return redirect(url_for("get_reviews"))
    
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Review Successfully Deleted")
    return redirect(url_for("get_reviews"))
