def test_global_order(client, mocker):
    test_club = [{"name": "test_name",
                  "email": "mail_user@valid.com",
                  "points": "20"}]
    mocker.patch('GUDLFT_app.server.clubs', test_club)

    test_event = [{"name": "test_event_name",
                   "date": "2024-01-01 10:00:00",
                   "numberOfPlaces": "15"}]
    mocker.patch('GUDLFT_app.server.competitions', test_event)

    rv = client.get("/")
    assert rv.status_code == 200

    rv = client.post(
        "/showSummary",
        data=dict(email=test_club[0]['email']), follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find("<title>Summary") != -1

    app_route = f"/book/{test_event[0]['name']}/{test_club[0]['name']}"
    print(app_route)
    rv = client.get(app_route, follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find('max="12"') != -1

    places = '10'

    rv = client.post(
        "/purchasePlaces",
        data=dict(club=test_club[0]['name'], competition=test_event[0]['name'], places=places),
        follow_redirects=True)

    assert rv.status_code == 200
    data = rv.data.decode()
    assert data.find('Great-booking complete') != -1
    assert data.find('<li>Great-booking complete : 10 places</li>') != -1
    assert data.find('Number of Places: 5') != -1

    rv = client.get('/logout', follow_redirects=True)
    data = rv.data.decode()

    assert rv.status_code == 200
    assert data.find('Please enter your secretary email to continue:') != -1