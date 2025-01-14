from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from db_instance import db
import utilities
from models import Fighter, FighterSchema, WeightClass, Match  # Updated schema with ordering
from collections import OrderedDict
from main import main


migrate = Migrate()

@main.route("/")
def home():
    return "Welcome to the UFC Collection Manager!"

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ufc.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Set a secret key 
    app.secret_key = "Mpx4GQmmNv"

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(main)

    return app


if __name__ == "__main__":
    app = create_app()
