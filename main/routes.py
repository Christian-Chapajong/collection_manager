from . import main
from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from db_instance import db
import utilities
from models import Fighter, FighterSchema, WeightClass, Match
from collections import OrderedDict
from sqlalchemy import or_
from datetime import datetime, date
from sqlalchemy.orm import aliased

# ===========================
# ======== Fighters =========
# ===========================
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
        return redirect(url_for("main.fighters"))

    # GET: Render an edit form pre-filled with fighter data
    return render_template("fighters_edit.html", fighter=fighter)

@main.route("/fighters/<int:fighter_id>/delete", methods=["POST"])
def delete_fighter(fighter_id):
    fighter = Fighter.query.get_or_404(fighter_id)
    db.session.delete(fighter)
    db.session.commit()

    flash(f"Fighter (ID: {fighter_id}) deleted!")
    return redirect(url_for("main.fighters"))

# ===========================
# ======== Matches ==========
# ===========================
@main.route("/matches", methods=["GET"])
def matches():
    # 1. Grab query params for filtering or searching
    fighter_name = request.args.get("fighter_name", "", type=str)
    weight_class = request.args.get("weight_class", "", type=str)
    date_str = request.args.get("date", "", type=str)
    
    page = request.args.get("page", 1, type=int)
    per_page = 25

    # 2. Base query
    query = Match.query

    # 3. Filter by fighter_name if provided
    # Match has fighter_1, fighter_2 relationships
    Fighter1 = aliased(Fighter)  # distinct alias for fighter1
    Fighter2 = aliased(Fighter)  # distinct alias for fighter2

    # explicit join on the same table with different aliases
    query = query.join(Fighter1, Match.fighter_1_id == Fighter1.id)
    query = query.join(Fighter2, Match.fighter_2_id == Fighter2.id)

    if fighter_name:
        query = query.filter(
            or_(
                Fighter1.name.ilike(f"%{fighter_name}%"),
                Fighter2.name.ilike(f"%{fighter_name}%")
            )
        )

    # 4. Filter by weight_class if provided
    if weight_class:
        query = query.filter(Match.weight_class_name.ilike(f"%{weight_class}%"))

    # 5. Filter by date
    if date_str:
        # parse date from string, for example "YYYY-MM-DD"
        try:
            from datetime import datetime
            match_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            query = query.filter(Match.date == match_date)
        except ValueError:
            flash("Invalid date format; use YYYY-MM-DD")

    # 6. Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # 7. Render a template "matches.html" with the pagination object
    return render_template("matches.html", pagination=pagination,
                           fighter_name=fighter_name, weight_class=weight_class,
                           date_str=date_str)

@main.route("/matches/new", methods=["GET", "POST"])
def new_match():
    if request.method == "POST":
        # 1. Read form data
        fighter_1_id = request.form.get("fighter_1_id", type=int)
        fighter_2_id = request.form.get("fighter_2_id", type=int)
        match_date_str = request.form.get("date")
        location = request.form.get("location")
        weight_class_name = request.form.get("weight_class_name")
        method = request.form.get("method", "Decision")
        round_ = request.form.get("round", 1, type=int)
        time_ = request.form.get("time", "")
        event_name = request.form.get("event_name", "")
        winner_id = request.form.get("winner_id", type=int)  # or None if no winner

        # parse date
        match_date = None
        if match_date_str:
            try:
                match_date = datetime.strptime(match_date_str, "%Y-%m-%d").date()
            except ValueError:
                flash("Invalid date format. Use YYYY-MM-DD.")
                return redirect(url_for("main.new_match"))

        # 2. Create the Match object
        new_match = Match(
            fighter_1_id=fighter_1_id,
            fighter_2_id=fighter_2_id,
            date=match_date,          # if your column is db.Date
            location=location,
            weight_class_name=weight_class_name,
            method=method,
            round=round_,
            time=time_,
            event_name=event_name,
            winner_id=winner_id
        )

        # 3. Insert into DB
        db.session.add(new_match)
        db.session.commit()

        flash("New match created!")
        return redirect(url_for("main.matches"))
    
    # GET request: render the "matches_new.html” template
    fighters=Fighter.query.all()
    weight_classes=WeightClass.query.all()
    return render_template("matches_new.html", fighters=fighters, weight_classes=weight_classes)
    
@main.route("/matches/<int:match_id>/edit", methods=["GET", "POST"])
def edit_match(match_id):
    match = Match.query.get_or_404(match_id)

    if request.method == "POST":
        match_date_str = request.form.get("date")
        match.location = request.form.get("location", match.location)
        match.weight_class_name = request.form.get("weight_class_name", match.weight_class_name)
        match.method = request.form.get("method", match.method)
        match.round = request.form.get("round", match.round, type=int)
        match.time = request.form.get("time", match.time)
        match.event_name = request.form.get("event_name", match.event_name)
        match.winner_id = request.form.get("winner_id", match.winner_id, type=int)

        # If user updates fighter_1/fighter_2
        fighter_1_id = request.form.get("fighter_1_id", type=int)
        if fighter_1_id:
            match.fighter_1_id = fighter_1_id

        fighter_2_id = request.form.get("fighter_2_id", type=int)
        if fighter_2_id:
            match.fighter_2_id = fighter_2_id

        # parse date
        if match_date_str:
            from datetime import datetime
            try:
                match.date = datetime.strptime(match_date_str, "%Y-%m-%d").date()
            except ValueError:
                flash("Invalid date format. Use YYYY-MM-DD.")

        db.session.commit()
        flash("Match updated successfully!")
        return redirect(url_for("main.matches"))

    # GET: show an edit form for the match
    fighters = Fighter.query.all()
    weight_classes = WeightClass.query.all()
    return render_template("match_edit.html", match=match, fighters=fighters, weight_classes=weight_classes)

@main.route("/matches/<int:match_id>/delete", methods=["POST"])
def delete_match(match_id):
    match = Match.query.get_or_404(match_id)
    db.session.delete(match)
    db.session.commit()

    flash(f"Match with ID {match_id} was deleted.")
    return redirect(url_for("main.matches"))

# ===========================
# ======= Analytics =========
# ===========================
@main.route("/analytics")
def analytics():
    ...