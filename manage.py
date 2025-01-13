import click
from flask import current_app
from flask.cli import with_appcontext
from models import Fighter, WeightClass, Match, FighterSchema
from flask_app import create_app
from db_instance import db
import utilities

app = create_app()

@app.cli.command("setup")
@with_appcontext
def init_db():
    """Deletes all rows from tables, but keeps the schema."""
    click.echo("Initializing the database...")

    # For each model you want to clear:
    db.session.query(Match).delete()
    db.session.query(Fighter).delete()
    db.session.query(WeightClass).delete()
   
    db.session.commit()
    click.echo("Database initialized.")
    """
    Loads data for fighters, weight classes, and matches 
    by calling utility methods that insert records into the DB.
    """
    click.echo("Loading fighter data...")
    utilities.init_fighter_table()

    click.echo("Loading weightclass data...")
    utilities.init_weightclass_table()

    click.echo("Loading match data...")
    utilities.init_match_table()

    click.echo("Data loaded successfully!")
