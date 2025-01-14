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
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
from math import pi

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
@main.route("/fighter_comparison", methods=["GET"])
def fighter_comparison():
    fighters = Fighter.query.all()
    return render_template("fighter_comparison.html", fighters=fighters)

@main.route('/analytics')
def analytics():
    # Get the selected fighter IDs from the query string
    fighter_1_id = request.args.get('fighter_1_id', type=int)
    fighter_2_id = request.args.get('fighter_2_id', type=int)
    
    # Retrieve fighter data based on selected fighter IDs
    fighter_1 = Fighter.query.get(fighter_1_id)
    fighter_2 = Fighter.query.get(fighter_2_id)

    if not fighter_1 or not fighter_2:
        flash("Invalid fighter(s) selected", "error")
        return redirect(url_for('main.index'))
    
    # Group 1: Wins, Losses, Draws
    wdl_stats = ["wins", "losses", "draws"]
    fighter_1_wdl = [getattr(fighter_1, stat) for stat in wdl_stats]
    fighter_2_wdl = [getattr(fighter_2, stat) for stat in wdl_stats]
    
    # Group 2: Height, Weight, Reach
    hw_reach_stats = ["height_cm", "weight_kg", "reach_cm"]
    fighter_1_hw_reach = [getattr(fighter_1, stat) for stat in hw_reach_stats]
    fighter_2_hw_reach = [getattr(fighter_2, stat) for stat in hw_reach_stats]
    
    # Group 3: Remaining Stats
    remaining_stats = [
        "significant_strikes_landed_per_minute", "significant_striking_accuracy",
        "significant_strikes_absorbed_per_minute", "significant_strike_defence",
        "average_takedowns_landed_per_15_minutes", "takedown_accuracy", 
        "takedown_defense", "average_submissions_attempted_per_15_minutes"
    ]
    fighter_1_remaining = [getattr(fighter_1, stat) for stat in remaining_stats]
    fighter_2_remaining = [getattr(fighter_2, stat) for stat in remaining_stats]
    
    # Labels
    wdl_labels = ["Wins", "Losses", "Draws"]
    hw_reach_labels = ["Height (cm)", "Weight (kg)", "Reach (cm)"]
    remaining_labels = [
        "Strikes per Minute", "Striking Accuracy", "Strikes Absorbed per Minute",
        "Strike Defence", "Takedowns per 15 Min", "Takedown Accuracy", "Takedown Defense",
        "Submissions per 15 Min"
    ]
    
    # Function to create bar chart and return base64 encoded image
    def create_bar_chart(labels, fighter_1_stats, fighter_2_stats, title):
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_width = 0.35
        index = np.arange(len(labels))
        
        bars1 = ax.bar(index, fighter_1_stats, bar_width, label=fighter_1.name)
        bars2 = ax.bar(index + bar_width, fighter_2_stats, bar_width, label=fighter_2.name)
        
        ax.set_xlabel('Statistics')
        ax.set_ylabel('Values')
        ax.set_title(title)
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.legend()

        # Save the plot as a PNG image
        img = BytesIO()
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode('utf8')

    # Generate charts for each group
    wdl_chart_data = create_bar_chart(wdl_labels, fighter_1_wdl, fighter_2_wdl, 'W/D/L Comparison')
    hw_reach_chart_data = create_bar_chart(hw_reach_labels, fighter_1_hw_reach, fighter_2_hw_reach, 'Height/Weight/Reach Comparison')
    remaining_stats_chart_data = create_bar_chart(remaining_labels, fighter_1_remaining, fighter_2_remaining, 'Remaining Stats Comparison')

    return render_template('analytics.html', 
                           fighter_1=fighter_1, 
                           fighter_2=fighter_2, 
                           wdl_chart_data=wdl_chart_data,
                           hw_reach_chart_data=hw_reach_chart_data,
                           remaining_stats_chart_data=remaining_stats_chart_data)