from models import Fighter, WeightClass, Match
from db_instance import db
import pandas as pd
from flask import current_app
from constants import WEIGHTCLASSES
from datetime import datetime

def read_csv_file(file_path):
    df = pd.read_csv(file_path)  # Read CSV into a DataFrame
    return df.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries

def parse_date(raw_value):
    """
    Safely parse date from raw_value, which might be float/NaN/etc.
    Expecting format: DD/MM/YYYY.
    """
    # If raw_value is None or float, skip or return None
    if not isinstance(raw_value, str):
        return None

    raw_value = raw_value.strip()
    if not raw_value:
        return None  # empty string

    try:
        return datetime.strptime(raw_value, "%d/%m/%Y").date()
    except ValueError:
        return None

def set_weightclass(weight):
    for class_name, limit in WEIGHTCLASSES:
        # Skip weight classes that have no valid weight limit (None or NaN)
        if limit is None or limit != limit:  # Checks if limit is NaN
            continue
        if weight <= limit:
            return class_name
    return "Super Heavyweight"

def init_fighter_table():
    with current_app.app_context():
        fighter_file = "data/UFC_Fighters.csv"
        fighters_data = read_csv_file(fighter_file)

        for fighter_data in fighters_data:
            fighter_weightclass = set_weightclass(fighter_data['weight_kg'])

            fighter = Fighter(
                name = fighter_data['name'],
                nickname = fighter_data.get('nickname', None),
                weight_class = fighter_weightclass,
                wins = fighter_data.get('wins', 0),
                draws = fighter_data.get('draws', 0),
                losses = fighter_data.get('losses', 0),
                height_cm = fighter_data.get('height_cm', 0.0),
                weight_kg = fighter_data.get('weight_kg', 0.0),
                reach_cm = fighter_data.get('reach_in_cm', 0.0),
                stance = fighter_data.get('stance', None),
                significant_strikes_landed_per_minute = fighter_data.get('significant_strikes_landed_per_minute', 0.0),
                significant_striking_accuracy = fighter_data.get('significant_striking_accuracy', 0.0),
                significant_strikes_absorbed_per_minute = fighter_data.get('significant_strikes_absorbed_per_minute', 0.0),
                significant_strike_defence = fighter_data.get('significant_strike_defence', 0),
                average_takedowns_landed_per_15_minutes = fighter_data.get('average_takedowns_landed_per_15_minutes', 0.0),
                takedown_accuracy = fighter_data.get('takedown_accuracy', 0),
                takedown_defense = fighter_data.get('takedown_defense', 0),
                average_submissions_attempted_per_15_minutes = fighter_data.get('average_submissions_attempted_per_15_minutes', 0.0),
                sex = fighter_data.get('sex', None)
            )

            db.session.add(fighter)

        db.session.commit()

def init_weightclass_table():
    for i in range(len(WEIGHTCLASSES)):
        if i == len(WEIGHTCLASSES) - 1:
            break
        
        # Check if the current weightclass has a valid min_weight and max_weight
        min_weight = WEIGHTCLASSES[i][1]
        next_weight = WEIGHTCLASSES[i+1][1]
        
        if min_weight is None:
            min_weight = 0  # or any appropriate value for missing min weight
        
        if next_weight is None:
            next_weight = float('inf')  # set max_weight to inf for missing next weight

        weightclass = WeightClass(
            name = WEIGHTCLASSES[i][0],
            min_weight = min_weight,
            max_weight = next_weight
        )

        db.session.add(weightclass)

    # Add the last weightclass
    last_weightclass = WEIGHTCLASSES[-1]
    min_weight = last_weightclass[1]
    
    if min_weight is None:
        min_weight = 0  # or any appropriate value for missing min weight

    weightclass = WeightClass(
        name = last_weightclass[0],
        min_weight = min_weight,
        max_weight = float('inf')  # Set max_weight to inf for the last weight class
    )

    db.session.commit()

def init_match_table():
    matches_file = "data/UFC_Matches.csv"
    matches_data = read_csv_file(matches_file)

    for match_data in matches_data:
        #TODO - get fighter_1_id and fighter_2_id from the Fighter table
        fighter_1 = db.session.query(Fighter).filter_by(name=match_data['fighter_1']).first()
        fighter_2 = db.session.query(Fighter).filter_by(name=match_data['fighter_2']).first()

        if not fighter_1 or not fighter_2:
            continue  # Skip this match if either fighter is not found

        match_data['fighter_1_id'] = fighter_1.id
        match_data['fighter_2_id'] = fighter_2.id
        
        match_data.get('fighter_1')

        # Set the winner_id based on the winner's name
        if match_data.get('winner') == match_data['fighter_1']:
            match_data['winner_id'] = fighter_1.id
        elif match_data.get('winner') == match_data['fighter_2']:
            match_data['winner_id'] = fighter_2.id
        else:
            match_data['winner_id'] = None

        # Convert date string -> Python date
        date_value = parse_date(match_data.get('date', None))

        match = Match(
            location=match_data.get('location', None),
            fighter_1_id=match_data.get('fighter_1_id', None),
            fighter_2_id=match_data.get('fighter_2_id', None),
            fighter_1_kd=match_data.get('fighter_1_kd', 0),
            fighter_2_kd=match_data.get('fighter_2_kd', 0),
            
            fighter_1_str=match_data.get('fighter_1_str', 0),
            fighter_2_str=match_data.get('fighter_2_str', 0),

            fighter_1_td=match_data.get('fighter_1_td', 0),
            fighter_2_td=match_data.get('fighter_2_td', 0),

            fighter_1_sub=match_data.get('fighter_1_sub_att', 0),
            fighter_2_sub=match_data.get('fighter_2_sub_att', 0),

            # Weight class by name (string)
            weight_class_name=match_data.get('weight_class', None),  # or any default

            # Method of victory, round, time, event_name, date
            method=match_data.get('method', 'Decision'),  # method is non-nullable, give a default
            round=match_data.get('round', 1),
            time=match_data.get('time', None),
            event_name=match_data.get('event_name', None),
            date=date_value,  # if your DB can handle a NULL date or handle it as a string
            winner_id=match_data.get('winner', None)
)


        db.session.add(match)
        
    db.session.commit()
