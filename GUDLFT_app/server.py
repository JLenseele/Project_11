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

    set_places = [int(club['points']), MAX_PLACES, int(competition['numberOfPlaces'])]
    return min(set_places)


def __purchase_register(club, competition, places):
    """
        Checks each order already register to accept or not the current order

        :param: competition: instance competitions
        :param: club: instance club
        :param: places: number of places in order
        :return: True or False
    """
    order_places = 0
    for register in purchase:
        if register[0] == club and register[1] == competition:
            order_places += register[2]

    total_places = order_places + places

    if total_places > MAX_PLACES:
        remaining = MAX_PLACES - order_places
        flash(f'Cancelled order ! You cannot order more than ({remaining}) places')
        return False
    else:
        purchase.append([club, competition, places])
        flash(f'Great-booking complete : {places} places')
        return True


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
purchase = []
MAX_PLACES = 12


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
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
    except IndexError:
        flash("Parameter missing, please try login again")
        return render_template('index.html')
    else:
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

    if 0 < placesRequired < int(club['points']) and placesRequired < int(competition['numberOfPlaces']):
        if __purchase_register(club['name'], competition['name'], placesRequired):
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club['points'] = int(club['points']) - placesRequired
    else:
        flash(f'({placesRequired}) - Number of places requested invalid')
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

