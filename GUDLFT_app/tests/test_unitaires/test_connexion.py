from GUDLFT_app.tests.conftest import client
from GUDLFT_app import server


def test_index_status_code_ok(client):
    response = client.get('/')
    assert response.status_code == 200


def _mocker_club(mocker):
    clubs = [{"email": "mail_user@valid.com"}]
    mocker.patch('GUDLFT_app.server.clubs', clubs)


def _login_user(client, email, valid=True):

    rv = client.post(
        "/showSummary",
        data=dict(email=email), follow_redirects=True)

    assert rv.status_code == 200

    data = rv.data.decode()
    if valid:
        assert data.find("<title>Summary") != -1
    else:
        assert data.find("<h4>Ce compte n&#39;existe pas</h4>") != -1


def test_showSummary_login_succes(client, mocker):
    _mocker_club(mocker)
    _login_user(client, "mail_user@valid.com")


def test_showSummary_login_fail(client, mocker):
    _mocker_club(mocker)
    _login_user(client, "mail_user@invalid.com", False)

