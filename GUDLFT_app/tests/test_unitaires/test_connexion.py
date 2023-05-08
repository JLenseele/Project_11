def test_index_status_code_ok(client):
    rv = client.get('/')
    assert rv.status_code == 200


def _mocker_club(mocker):
    clubs = [{"name": "test_name",
              "email": "mail_user@valid.com",
              "points": "20"}]
    mocker.patch('GUDLFT_app.server.clubs', clubs)


def _login_user(client, email):

    rv = client.post(
        "/showSummary",
        data=dict(email=email), follow_redirects=True)

    assert rv.status_code == 200

    data = rv.data.decode()
    return data


def test_showSummary_login_succes(client, mocker):
    _mocker_club(mocker)
    data = _login_user(client, "mail_user@valid.com")
    assert data.find("<title>Summary") != -1


def test_showSummary_login_fail(client, mocker):
    _mocker_club(mocker)
    data = _login_user(client, "mail_user@invalid.com")
    assert data.find("<h4>Ce compte n&#39;existe pas</h4>") != -1


def test_logout(client):
    rv = client.get('/logout', follow_redirects=True)
    data = rv.data.decode()

    assert rv.status_code == 200
    assert data.find('Please enter your secretary email to continue:') != -1
