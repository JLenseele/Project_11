import pytest

import GUDLFT_app.server


def test_load_clubs():
    clubs = GUDLFT_app.server.loadClubs()
    assert len(clubs) > 0
    assert clubs[0]['name'] == 'Simply Lift'
    assert clubs[0]['email'] == 'john@simplylift.co'
    assert clubs[0]['points'] == '13'


def test_load_competitions():
    competitions = GUDLFT_app.server.loadCompetitions()
    assert len(competitions) > 0
    assert competitions[0]['name'] == 'Spring Festival'
    assert competitions[0]['date'] == '2020-03-27 10:00:00'
    assert competitions[0]['numberOfPlaces'] == '25'
