from models import Fighter
from db_instance import db
import pandas as pd

def read_csv_file(file_path):
    df = pd.read_csv(file_path)  # Read CSV into a DataFrame
    return df.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries

def set_weightclass(weight):
    if weight <= 52.2:
        return 'Stawweight'
    elif weight <= 56.7:
        return 'Flyweight'
    elif weight <= 61.2:
        return 'Bantaweight'
    elif weight <= 65.8:
        return 'Featherweight'
    elif weight <= 70.3:
        return 'Lightweight'
    elif weight <= 74.8:
        return 'Super lightweight'
    elif weight <= 77.1:
        return 'Welterweight'
    elif weight <= 79.4:
        return 'Super welterweight'
    elif weight <= 83.9:
        return 'Middleweight'
    elif weight <= 88.5:
        return 'Super middleweight'
    elif weight <= 93.0:
        return 'Light heavyweight'
    elif weight <= 102.1:
        return 'Cruiserweight'
    elif weight <= 120.2:
        return 'Heavyweight'
    else:
        return 'Super heavweight'

def init_db():
    file_path = "data/UFC_Fighters.csv"
    fighters_data = read_csv_file(file_path)

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

