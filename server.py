import json
from urllib.error import HTTPError

import urllib3
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = \
            [club for club in clubs if club['email'] == request.form['email']][
                0]
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)
    except IndexError:
        flash(f"This email is not valid, please enter a new email")
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        competitionDate = datetime.strptime(foundCompetition['date'][0:10],
                                            "%Y-%m-%d").date()
        date = datetime.now().date()
        result = competitionDate > date
        if foundClub and foundCompetition:
            if result:
                return render_template('booking.html', club=foundClub,
                                       competition=foundCompetition)
            else:
                flash("This is a past competition, reservation is not "
                      "available")
                club = foundClub
                return render_template('welcome.html', club=club,
                                       competitions=competitions)
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template('index.html')


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = \
        [c for c in competitions if c['name'] == request.form['competition']][
            0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    if placesRequired > int(competition['numberOfPlaces']):
        flash(f"Not enough places left. You can book at most "
              f"{competition['numberOfPlaces']} places")
        return render_template('booking.html', club=club,
                               competition=competition)
    elif placesRequired > 12:
        flash("It's not possible to book more than twelve places.")
        return render_template('booking.html', club=club,
                               competition=competition)
    elif placesRequired <= int(club["points"]):
        club["points"] = int(club["points"]) - placesRequired
        competition['numberOfPlaces'] = \
            int(competition['numberOfPlaces']) - placesRequired
        flash('Great-booking complete!')
        flash(f'{placesRequired} places reserved')
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    else:
        flash('Not enough points to book')
        return render_template('welcome.html', club=club,
                               competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
