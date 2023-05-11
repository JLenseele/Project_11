def _mocker_club(mocker):
    clubs = [{"name": "test_name",
              "email": "mail_user@valid.com",
              "points": "20"}]
    mocker.patch('GUDLFT_app.server.clubs', clubs)


def _mocker_competition(mocker):
    competitions = [{"name": "test_competition",
                     "date": "2024-10-22 13:30:00",
                     "numberOfPlaces": "20"}]
    mocker.patch('GUDLFT_app.server.competitions', competitions)


def _post_showSummary(client, mocker):

    _mocker_club(mocker)
    rv = client.post(
        "/showSummary",
        data=dict(email='mail_user@valid.com'), follow_redirects=True)

    data = rv.data.decode()
    return data, rv


def test_set_max_places_12(client, mocker):
    clubs = [{"name": "test_club",
              "email": "mail_user@valid.com",
              "points": "20"}]
    mocker.patch('GUDLFT_app.server.clubs', clubs)

    competitions = [{"name": "test_competition",
                     "date": "2024-10-22 13:30:00",
                     "numberOfPlaces": "20"}]
    mocker.patch('GUDLFT_app.server.competitions', competitions)

    app_route = f"/book/{competitions[0]['name']}/{clubs[0]['name']}"
    print(app_route)
    rv = client.get(app_route, follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find('max="12"') != -1


def test_set_max_places_club_points(client, mocker):
    clubs = [{"name": "test_club",
              "email": "mail_user@valid.com",
              "points": "5"}]
    mocker.patch('GUDLFT_app.server.clubs', clubs)

    competitions = [{"name": "test_competition",
                     "date": "2024-10-22 13:30:00",
                     "numberOfPlaces": "20"}]
    mocker.patch('GUDLFT_app.server.competitions', competitions)

    app_route = f"/book/{competitions[0]['name']}/{clubs[0]['name']}"
    print(app_route)
    rv = client.get(app_route, follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find('max="5"') != -1


def test_set_max_places_competition_points(client, mocker):
    clubs = [{"name": "test_club",
              "email": "mail_user@valid.com",
              "points": "20"}]
    mocker.patch('GUDLFT_app.server.clubs', clubs)

    competitions = [{"name": "test_competition",
                     "date": "2024-10-22 13:30:00",
                     "numberOfPlaces": "4"}]
    mocker.patch('GUDLFT_app.server.competitions', competitions)

    app_route = f"/book/{competitions[0]['name']}/{clubs[0]['name']}"
    rv = client.get(app_route, follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find('max="4"') != -1


def test_error_book_url(client, mocker):
    app_route = f"/book/event_invalid_name/club_invalid_name"
    rv = client.get(app_route, follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find('Parameter missing, please try login again') != -1


def test_event_valid(client, mocker):

    test_event = [{"name": "test_event_name",
                   "date": "2024-01-01 10:00:00",
                   "numberOfPlaces": "10"}]
    mocker.patch('GUDLFT_app.server.competitions', test_event)

    data, rv = _post_showSummary(client, mocker)

    assert rv.status_code == 200
    assert data.find("Book Places") != -1


def test_event_date_passed(client, mocker):
    test_event = [{"name": "test_event_name",
                   "date": "2015-01-01 10:00:00",
                   "numberOfPlaces": "10"}]
    mocker.patch('GUDLFT_app.server.competitions', test_event)

    data, rv = _post_showSummary(client, mocker)

    assert rv.status_code == 200
    assert data.find("Reservations are unavailable for this event") != -1


def test_event_place_unvailable(client, mocker):
    test_event = [{"name": "test_event_name",
                   "date": "2024-01-01 10:00:00",
                   "numberOfPlaces": "0"}]
    mocker.patch('GUDLFT_app.server.competitions', test_event)

    data, rv = _post_showSummary(client, mocker)

    assert rv.status_code == 200
    assert data.find("Reservations are unavailable for this event") != -1


def test_club_point_unvailable(client, mocker):
    test_event = [{"name": "test_event_name",
                   "date": "2024-01-01 10:00:00",
                   "numberOfPlaces": "20"}]
    mocker.patch('GUDLFT_app.server.competitions', test_event)

    clubs = [{"name": "test_club",
              "email": "mail_user@valid.com",
              "points": "0"}]
    mocker.patch('GUDLFT_app.server.clubs', clubs)

    rv = client.post(
        "/showSummary",
        data=dict(email='mail_user@valid.com'), follow_redirects=True)

    data = rv.data.decode()

    assert rv.status_code == 200
    assert data.find("Your club does not have enough points to book") != -1
