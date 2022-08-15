from surfproject import db


class User(db.Model):
    #schema for the user
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(25), unique=True, nullable=False)
    user_email = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    reviews = db.relationship("Review", backref="user", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.user_name


class Review(db.Model):
    #schema for the reviews
    id = db.Column(db.Integer, primary_key=True)
    camp_name = db.Column(db.String(100), nullable=False)
    camp_id = db.Column(db.Integer, db.ForeignKey("camps.id", ondelete="CASCADE"), nullable=False)
    camp_rating = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(25), db.ForeignKey("user.user_name", ondelete="CASCADE"), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    camps = db.relationship("Camps", backref="review", cascade="all, delete", lazy=True)


    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#Camp: {0} - Rating: {1} | Author: {2}".format(
            self.camp_name, self.camp_rating, self.user_name
        )


class Countries(db.Model):
    #schema for the countries used in overview per country
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(30), nullable=False)
    campcountries = db.relationship("Camps", backref="countries", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.country_name


class Camps(db.Model):
    #schema for the camps overview
    id = db.Column(db.Integer, primary_key=True)
    average_rating = (db.Integer)
    camp_name = (db.String, db.ForeignKey("review.camp_name", ondelete="CASCADE"))
    country_name = (db.String, db.ForeignKey("countries.country_name", ondelete="CASCADE"))
    campreviews = db.relationship("Review", backref="camps", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.camp_name