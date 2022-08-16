from surfproject import db

class Review(db.Model):
    #schema for the reviews
    id = db.Column(db.Integer, primary_key=True)
    camp_name = db.Column(db.String(100), nullable=False)
    camp_country = db.Column(db.String(100), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    camps = db.relationship("Camps", back_populates="review")

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#Camp: {0} - Country: {1}".format(
            self.camp_name, self.camp_country
        )


class Camps(db.Model):
    #schema for the camps overview
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"))
    reviews = db.relationship("Review", back_populates="camps")

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.camp_name