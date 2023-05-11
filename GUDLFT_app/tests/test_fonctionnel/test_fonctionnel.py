import time
from GUDLFT_app.server import app
from flask_testing import LiveServerTestCase
from selenium import webdriver


class TestGlobalOrder(LiveServerTestCase):
    def create_app(self):
        # Fichier de config de test fonctionnel
        app.config.from_object('GUDLFT_app.tests.test_fonctionnel.config')
        return app

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test_user_login(self):
        self.driver.get(self.get_server_url())
        assert self.driver.current_url == "http://localhost:8943"