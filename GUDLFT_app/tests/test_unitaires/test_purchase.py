def _mocker_club_valid(mocker):
    clubs = [{"name": "test_name",
              "email": "mail_user@valid.com",
              "points": "20"}]
    mocker.patch('GUDLFT_app.server.clubs', clubs)


def _mocker_club_low_points(mocker):
    clubs = [{"name": "test_name",
              "email": "mail_user@valid.com",
              "points": "2"}]
    mocker.patch('GUDLFT_app.server.clubs', clubs)


def _mocker_competition_valid(mocker):
    competitions = [{"name": "test_competition",
                     "date": "2024-10-22 13:30:00",
                     "numberOfPlaces": "20"}]
    mocker.patch('GUDLFT_app.server.competitions', competitions)


def _mocker_competition_low_places(mocker):
    competitions = [{"name": "test_competition",
                     "date": "2024-10-22 13:30:00",
                     "numberOfPlaces": "2"}]
    mocker.patch('GUDLFT_app.server.competitions', competitions)


def _mocker_purchase(mocker):
    purchase = [('test_name', 'test_competition', 8)]
    mocker.patch('GUDLFT_app.server.purchase', purchase)


def test_purchase_valid_(client, mocker):

    _mocker_club_valid(mocker)
    _mocker_competition_valid(mocker)

    club = 'test_name'
    competition = 'test_competition'
    places = '2'

    rv = client.post(
        "/purchasePlaces",
        data=dict(club=club, competition=competition, places=places),
        follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find('Great-booking complete') != -1


def test_purchase_invalid_number(client, mocker):

    _mocker_club_valid(mocker)
    _mocker_competition_valid(mocker)

    club = 'test_name'
    competition = 'test_competition'
    places = '-2'

    rv = client.post(
        "/purchasePlaces",
        data=dict(club=club, competition=competition, places=places),
        follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find('Number of places requested invalid') != -1


def test_purchase_not_enough_point(client, mocker):

    _mocker_club_low_points(mocker)
    _mocker_competition_valid(mocker)

    club = 'test_name'
    competition = 'test_competition'
    places = '10'

    rv = client.post(
        "/purchasePlaces",
        data=dict(club=club, competition=competition, places=places),
        follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find('Number of places requested invalid') != -1


def test_purchase_not_enough_places(client, mocker):

    _mocker_club_valid(mocker)
    _mocker_competition_low_places(mocker)

    club = 'test_name'
    competition = 'test_competition'
    places = '10'

    rv = client.post(
        "/purchasePlaces",
        data=dict(club=club, competition=competition, places=places),
        follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find('Number of places requested invalid') != -1


def test_multiple_purchase_valid(client, mocker):

    _mocker_club_valid(mocker)
    _mocker_competition_valid(mocker)
    _mocker_purchase(mocker)

    club = 'test_name'
    competition = 'test_competition'
    places = '2'

    rv = client.post(
        "/purchasePlaces",
        data=dict(club=club, competition=competition, places=places),
        follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find('Great-booking complete : 2 places') != -1


def test_multiple_purchase_invalid(client, mocker):

    _mocker_club_valid(mocker)
    _mocker_competition_valid(mocker)
    _mocker_purchase(mocker)

    club = 'test_name'
    competition = 'test_competition'
    places = '6'

    rv = client.post(
        "/purchasePlaces",
        data=dict(club=club, competition=competition, places=places),
        follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find('Cancelled order ! You cannot order more than (4) places') != -1
