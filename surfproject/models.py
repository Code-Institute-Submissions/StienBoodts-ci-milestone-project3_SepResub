from surfproject import db


class Camps(db.Model):
    #schema for the camps overview
    id = db.Column(db.Integer, primary_key=True)
    camp_name = db.Column(db.String(100), unique=True, nullable=False)
    reviews = db.relationship("Review", backref="camps", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.camp_name


class Review(db.Model):
    #schema for the reviews
    id = db.Column(db.Integer, primary_key=True)
    review_name = db.Column(db.String(50), unique=True, nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    camp_id = db.Column(db.Integer, db.ForeignKey("camps.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Name: {1} | Review: {2}".format(
            self.id, self.review_name, self.review_text
        )
