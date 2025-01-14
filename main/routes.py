from . import main
from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from db_instance import db
import utilities
from models import Fighter, FighterSchema, WeightClass, Match
from collections import OrderedDict

@main.route("/fighters", methods=["GET"])
def fighters():
    # 1. Grab the 'search' term from query params
    search_term = request.args.get("search", "", type=str)
    
    # 2. Grab 'page' for pagination
    page = request.args.get("page", 1, type=int)
    per_page = 25

    # 3. Start a base query
    query = Fighter.query

    # 4. If there's a search term, filter by fighter name (case-insensitive)
    if search_term:
        # Example of filtering by name
        query = query.filter(Fighter.name.ilike(f"%{search_term}%"))

    # 5. Paginate the resulting query
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # 6. Render the fighters.html template
    #    Pass pagination object & current search term to the template
    return render_template("fighters.html", pagination=pagination, search=search_term)

@main.route("/fighters/new", methods=["GET", "POST"])
def new_fighter():
    if request.method == "POST":
        # 1. Read form data
        name = request.form.get('name')
        nickname = request.form.get('nickname')
        weight_class = request.form.get('weight_class')
        wins = request.form.get('wins', 0, type=int)
        draws = request.form.get('draws', 0, type=int)
        losses = request.form.get('losses', 0, type=int)
        stance = request.form.get('stance')
        height_cm = request.form.get('height_cm', 0, type=float)
        reach_cm = request.form.get('reach_cm', 0, type=float)
        sex = request.form.get('sex')

        # 2. Basic validation
        if not name or not weight_class:
            flash("Name and Weight Class are required.")
            return redirect(url_for('main.new_fighter'))

        # 3. Create the Fighter
        new_fighter = Fighter(
            name=name,
            nickname=nickname,
            weight_class=weight_class,
            wins=wins,
            draws=draws,
            losses=losses,
            stance=stance,
            height_cm=height_cm,
            reach_cm=reach_cm,
            sex=sex
            # Add any other fields you want to capture here
        )

        # 4. Save to DB
        db.session.add(new_fighter)
        db.session.commit()

        # 5. Flash success & redirect to /fighters
        flash(f"Fighter '{name}' created successfully!")
        return redirect(url_for('main.fighters'))

    # GET request: render the “fighters_new.html” template
    return render_template("fighters_new.html")


@main.route("/fighters/<int:fighter_id>/edit", methods=["GET", "POST"])
def edit_fighter(fighter_id):
    fighter = Fighter.query.get_or_404(fighter_id)

    if request.method == "POST":
        # Read updated fields from form
        fighter.name = request.form.get("name", fighter.name)
        fighter.nickname = request.form.get("nickname", fighter.nickname)
        fighter.weight_class = request.form.get("weight_class", fighter.weight_class)
        fighter.wins = request.form.get("wins", fighter.wins, type=int)
        fighter.losses = request.form.get("losses", fighter.losses, type=int)
        fighter.draws = request.form.get("draws", fighter.draws, type=int)
        fighter.height_cm = request.form.get("height_cm", fighter.height_cm, type=float)
        fighter.weight_kg = request.form.get("weight_kg", fighter.weight_kg, type=float)
        fighter.reach_cm = request.form.get("reach_cm", fighter.reach_cm, type=float)
        fighter.stance = request.form.get("stance", fighter.stance)
        fighter.significant_strikes_landed_per_minute = request.form.get("significant_strikes_landed_per_minute", fighter.significant_strikes_landed_per_minute, type=float)
        fighter.significant_striking_accuracy = request.form.get("significant_striking_accuracy", fighter.significant_striking_accuracy, type=float)
        fighter.significant_strikes_absorbed_per_minute = request.form.get("significant_strikes_absorbed_per_minute", fighter.significant_strikes_absorbed_per_minute, type=float)
        fighter.significant_strike_defence = request.form.get("significant_strike_defence", fighter.significant_strike_defence, type=float)
        fighter.average_takedowns_landed_per_15_minutes = request.form.get("average_takedowns_landed_per_15_minutes", fighter.average_takedowns_landed_per_15_minutes, type=float)
        fighter.takedown_accuracy = request.form.get("takedown_accuracy", fighter.takedown_accuracy, type=float)
        fighter.takedown_defense = request.form.get("takedown_defense", fighter.takedown_defense, type=float)
        fighter.average_submissions_attempted_per_15_minutes = request.form.get("average_submissions_attempted_per_15_minutes", fighter.average_submissions_attempted_per_15_minutes, type=float)
        fighter.sex = request.form.get("sex", fighter.sex)

        db.session.commit()
        flash(f"Fighter {fighter.name} updated successfully!")
        return redirect(url_for("main.fighters"))  # or some detail page

    # GET: Render an edit form pre-filled with fighter data
    return render_template("fighters_edit.html", fighter=fighter)

@main.route("/fighters/<int:fighter_id>/delete", methods=["POST"])
def delete_fighter(fighter_id):
    fighter = Fighter.query.get_or_404(fighter_id)
    db.session.delete(fighter)
    db.session.commit()

    flash(f"Fighter (ID: {fighter_id}) deleted!")
    return redirect(url_for("main.fighters"))