from datetime import date
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from db_instance import db

class Fighter(db.Model):
    """
    Fighter model. No references back to Match,
    so we avoid circular imports/definitions.
    """
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
    """
    Marshmallow schema for serializing Fighter objects.
    Ensures field order as declared.
    """
    class Meta:
        model = Fighter
        ordered = True

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


class WeightClass(db.Model):
    """
    WeightClass model with 'name' as primary key.
    No references back to Match, to avoid circular definitions.
    """
    __tablename__ = 'weight_classes'

    name = db.Column(db.String(50), primary_key=True)
    min_weight = db.Column(db.Float, nullable=False)
    max_weight = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<WeightClass(name='{self.name}', min_weight={self.min_weight}, max_weight={self.max_weight})>"


class Match(db.Model):
    """
    Matches hold references to Fighter and WeightClass, 
    but 'Fighter' and 'WeightClass' do not reference 'Match'
    (one-sided relationships).
    """
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=True)

    # Fighter references
    fighter_1_id = db.Column(db.Integer, db.ForeignKey('fighters.id'), nullable=False)
    fighter_2_id = db.Column(db.Integer, db.ForeignKey('fighters.id'), nullable=False)
    
    # Stats
    # Knockdowns, significant strikes, takedowns, submissions
    fighter_1_kd = db.Column(db.Integer, default=0)
    fighter_2_kd = db.Column(db.Integer, default=0)
    
    fighter_1_str = db.Column(db.Integer, default=0)
    fighter_2_str = db.Column(db.Integer, default=0)
    
    fighter_1_td = db.Column(db.Integer, default=0)
    fighter_2_td = db.Column(db.Integer, default=0)
    
    fighter_1_sub = db.Column(db.Integer, default=0)
    fighter_2_sub = db.Column(db.Integer, default=0)

    # WeightClass reference by name
    weight_class_name = db.Column(db.String(50), db.ForeignKey('weight_classes.name'), nullable=False)

    # Method of victory, round, etc.
    method = db.Column(db.String(50), nullable=False)  # KO, Submission, Decision...
    round = db.Column(db.Integer, default=1)
    time = db.Column(db.String(10), nullable=True)
    event_name = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date, default=date.today)
    winner_id = db.Column(db.Integer, db.ForeignKey('fighters.id'), nullable=True)

    # Single-sided relationships
    fighter_1 = db.relationship('Fighter', foreign_keys=[fighter_1_id])
    fighter_2 = db.relationship('Fighter', foreign_keys=[fighter_2_id])
    winner_rel = db.relationship('Fighter', foreign_keys=[winner_id])
    weight_class_rel = db.relationship('WeightClass')

    def __repr__(self):
        return f"<Match id={self.id}, event='{self.event_name}', date={self.date}>"
