import json
from flask import Flask, render_template, request, redirect, flash, url_for

from datetime import datetime


def loadClubs():
    """Return the list of all clubs"""
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    """Return the list of all competitions"""
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def __competition_is_valid(competitions):
    """
        Check if each competition are already passed or no
        & add keyword 'valid' set on True or False

        :param: competitions: list of competitions
        :return: list of competitions
    """
    for c in competitions:
        c_date = datetime.strptime(c['date'], '%Y-%m-%d %H:%M:%S')
        if c_date < datetime.now():
            c['valid'] = False
        else:
            c['valid'] = True
    return competitions


def __set_max_places(club, competition):
    """
            Set the number of places that can be reserved

            :param: competition: instance competitions
            :param: club: instance club
            :return: the minimum value in set_places list
        """
    max_places = 12
    set_places = [int(club['points']), max_places, int(competition['numberOfPlaces'])]
    return min(set_places)


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    """Return index.html template"""
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    """
        Check if (request.form['email']) exist in clubs email
        &
        Check each competition in __competition_is_valid()

        Exist:return: welcome.html template
        Not exist:return: index.html template with error message
    """
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        competitionsChecked = __competition_is_valid(competitions)
    except IndexError:
        return render_template('index.html', error="Ce compte n'existe pas")
    return render_template('welcome.html',
                           club=club,
                           competitions=competitionsChecked,
                           listclubs=clubs)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """
        Recover club & competition instance
        determines the maximum number of reserved places in __set_max_places

        :param: competitions: list of competitions
        :param: club: list of clubs

        Found club & competition
        :return: booking.html template
        Not found club & competition
        :return: welcome.html template with error message
    """
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    if foundClub and foundCompetition:
        max_places = __set_max_places(foundClub, foundCompetition)
        return render_template('booking.html',
                               club=foundClub,
                               competition=foundCompetition,
                               max=max_places)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """
        Recover club & competition instance
        & subtract places booking from competition and club points

        :return: welcome.html template with validation message
    """
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points']) - placesRequired

    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display
@app.route('/pointSummary')
def pointSummary():
    """ return summary template, to shows the number of points each club has """
    return render_template('summary.html', club=clubs)


@app.route('/logout')
def logout():
    """logout/redirect the curent user"""
    return redirect(url_for('index'))

