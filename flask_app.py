from flask import Flask, Blueprint, jsonify
from flask_migrate import Migrate
from flasgger import Swagger, swag_from
from db_instance import db
import utilities
from models import Fighter, FighterSchema  # Updated schema with ordering
from collections import OrderedDict

migrate = Migrate()
main = Blueprint("main", __name__)

@main.route("/")
def home():
    return "Welcome to the UFC Collection Manager!"

@main.route('/fighters', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'A list of all UFC fighters',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': OrderedDict([
                        ('id', {'type': 'integer'}),
                        ('name', {'type': 'string'}),
                        ('nickname', {'type': 'string'}),
                        ('weight_class', {'type': 'string'}),
                        ('wins', {'type': 'integer'}),
                        ('draws', {'type': 'integer'}),
                        ('losses', {'type': 'integer'}),
                        ('height_cm', {'type': 'number'}),
                        ('weight_kg', {'type': 'number'}),
                        ('reach_cm', {'type': 'number'}),
                        ('stance', {'type': 'string'}),
                        ('significant_strikes_landed_per_minute', {'type': 'number'}),
                        ('significant_striking_accuracy', {'type': 'number'}),
                        ('significant_strikes_absorbed_per_minute', {'type': 'number'}),
                        ('significant_strike_defence', {'type': 'integer'}),
                        ('average_takedowns_landed_per_15_minutes', {'type': 'number'}),
                        ('takedown_accuracy', {'type': 'integer'}),
                        ('takedown_defense', {'type': 'integer'}),
                        ('average_submissions_attempted_per_15_minutes', {'type': 'number'}),
                        ('sex', {'type': 'string'})
                    ])
                }
            }
        }
    }
})
def get_fighters():
    # Initialize DB/tables first if needed
    utilities.init_db()

    fighters = Fighter.query.all()
    # schema = FighterSchema(many=True)
    # data = schema.dump(fighters)  # Returns a list of dicts in the order declared
    # return jsonify(data)
    res = []
    for f in fighters:
        # Build an OrderedDict in the exact order you want
        od = OrderedDict()
        od['id'] = f.id
        od['name'] = f.name
        od['nickname'] = f.nickname
        od['weight_class'] = f.weight_class
        od['wins'] = f.wins
        od['draws'] = f.draws
        od['losses'] = f.losses
        od['height_cm'] = f.height_cm
        od['weight_kg'] = f.weight_kg
        od['reach_cm'] = f.reach_cm
        od['stance'] = f.stance
        od['significant_strikes_landed_per_minute'] = f.significant_strikes_landed_per_minute
        od['significant_striking_accuracy'] = f.significant_striking_accuracy
        od['significant_strikes_absorbed_per_minute'] = f.significant_strikes_absorbed_per_minute
        od['significant_strike_defence'] = f.significant_strike_defence
        od['average_takedowns_landed_per_15_minutes'] = f.average_takedowns_landed_per_15_minutes
        od['takedown_accuracy'] = f.takedown_accuracy
        od['takedown_defense'] = f.takedown_defense
        od['average_submissions_attempted_per_15_minutes'] = f.average_submissions_attempted_per_15_minutes
        od['sex'] = f.sex

        res.append(od)

    return jsonify(res)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ufc.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SWAGGER"] = {
        "swagger": "2.0",
        "info": {
            "title": "UFC Collection Manager API",
            "description": "API for managing UFC fighters, matches, and weight classes.",
            "version": "1.0.0",
        },
    }
    db.init_app(app)
    migrate.init_app(app, db)
    swagger = Swagger(app)
    app.register_blueprint(main)

    return app

if __name__ == "__main__":
    app = create_app()
