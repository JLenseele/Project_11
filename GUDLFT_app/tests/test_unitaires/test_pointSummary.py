def test_pointSummary(client, mocker):
    clubs = [{"name": "test_name",
              "email": "mail_user@valid.com",
              "points": "20"}]
    mocker.patch('GUDLFT_app.server.clubs', clubs)

    rv = client.get('/pointSummary', follow_redirects=True)
    data = rv.data.decode()

    assert rv.status_code == 200
    assert data.find('test_name') != -1
    assert data.find('Point: 20') != -1