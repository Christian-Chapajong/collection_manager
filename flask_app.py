from flask import Flask, Blueprint, jsonify, render_template, request
from flask_migrate import Migrate
from db_instance import db
import utilities
from models import Fighter, FighterSchema, WeightClass, Match  # Updated schema with ordering
from collections import OrderedDict

migrate = Migrate()
main = Blueprint("main", __name__)

@main.route("/")
def home():
    return "Welcome to the UFC Collection Manager!"

@main.route('/fighters', methods=['GET'])
def get_fighters():
    # fighters = Fighter.query.all()  # List of Fighter objects
    # schema = FighterSchema(many=True)
    # data = schema.dump(fighters)  # returns list of dicts
    # return jsonify(data)
    page = request.args.get("page", 1, type=int)
    per_page = 50

    pagination = Fighter.query.paginate(page=page, per_page=per_page, error_out=False)

    # Render the template 'fighters.html', passing the pagination object
    return render_template("fighters.html", pagination=pagination)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ufc.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(main)

    return app


if __name__ == "__main__":
    app = create_app()
