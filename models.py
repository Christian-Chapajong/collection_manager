from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from db_instance import db

class Fighter(db.Model):
    __tablename__ = 'fighters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(255))
    weight_class = db.Column(db.String(255), nullable=False)
    wins = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    height_cm = db.Column(db.Float, default=0)
    weight_kg = db.Column(db.Float, default=0)
    reach_cm = db.Column(db.Float, default=0)
    stance = db.Column(db.String(255))
    significant_strikes_landed_per_minute = db.Column(db.Float, default=0)
    significant_striking_accuracy = db.Column(db.Float, default=0)
    significant_strikes_absorbed_per_minute = db.Column(db.Float, default=0)
    significant_strike_defence = db.Column(db.Float, default=0)
    average_takedowns_landed_per_15_minutes = db.Column(db.Float, default=0)
    takedown_accuracy = db.Column(db.Float, default=0)
    takedown_defense = db.Column(db.Float, default=0)
    average_submissions_attempted_per_15_minutes = db.Column(db.Float, default=0)
    sex = db.Column(db.String(255))


    def __repr__(self):
        return f"<Fighter(name='{self.name}', weight_class='{self.weight_class}')>"

class FighterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fighter
        ordered = True  # Ensures fields appear in the order they are declared.

    # Declare fields in the exact order you want them to appear:
    id = auto_field()
    name = auto_field()
    nickname = auto_field()
    weight_class = auto_field()
    wins = auto_field()
    draws = auto_field()
    losses = auto_field()
    height_cm = auto_field()
    weight_kg = auto_field()
    reach_cm = auto_field()
    stance = auto_field()
    significant_strikes_landed_per_minute = auto_field()
    significant_striking_accuracy = auto_field()
    significant_strikes_absorbed_per_minute = auto_field()
    significant_strike_defence = auto_field()
    average_takedowns_landed_per_15_minutes = auto_field()
    takedown_accuracy = auto_field()
    takedown_defense = auto_field()
    average_submissions_attempted_per_15_minutes = auto_field()
    sex = auto_field()
# class WeightClass(db.Model):
#     """
#     WeightClass model representing UFC weight divisions.
#     """
#     __tablename__ = 'weight_classes'

#     name = db.Column(db.String(50), primary_key=True)
#     min_weight = db.Column(db.Float, nullable=False)
#     max_weight = db.Column(db.Float, nullable=False)

#     # Relationships
#     fighters = db.relationship('Fighter', back_populates='weight_class_relation')
#     matches = db.relationship('Match', back_populates='weight_class_relation')

#     def __repr__(self):
#         return f"<WeightClass(name='{self.name}', min_weight={self.min_weight}, max_weight={self.max_weight})>"


# class Match(db.Model):
#     """
#     Match model representing individual UFC fights.
#     """
#     __tablename__ = 'matches'

#     id = db.Column(db.Integer, primary_key=True)
#     match_date = db.Column(db.Date, nullable=False)
#     weight_class = db.Column(db.String(50), db.ForeignKey('weight_classes.name'), nullable=False)
#     fighter1_id = db.Column(db.Integer, db.ForeignKey('fighters.id'), nullable=False)
#     fighter2_id = db.Column(db.Integer, db.ForeignKey('fighters.id'), nullable=False)
#     winner_id = db.Column(db.Integer, db.ForeignKey('fighters.id'), nullable=True)  # Winner FK, nullable if draw or no contest
#     method = db.Column(db.String(50), nullable=False)  # e.g., KO, Submission, Decision

#     # Relationships
#     fighter1 = db.relationship('Fighter', foreign_keys=[fighter1_id], back_populates='matches_as_fighter1')
#     fighter2 = db.relationship('Fighter', foreign_keys=[fighter2_id], back_populates='matches_as_fighter2')
#     winner = db.relationship('Fighter', foreign_keys=[winner_id], back_populates='matches_as_winner')
#     weight_class_relation = db.relationship('WeightClass', back_populates='matches')

#     def __repr__(self):
#         return f"<Match(fighter1_id={self.fighter1_id}, fighter2_id={self.fighter2_id}, winner_id={self.winner_id}, method='{self.method}')>"
