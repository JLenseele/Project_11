import os
SECRET_KEY = 'something_special'

# Remplacez par l'id de l'app TEST que vous avez créée précédemment.
FB_APP_ID = 12345678901234567890

basedir = os.path.abspath(os.path.dirname(__file__))

# Active le debogueur
DEBUG = True
TESTING = True
LIVESERVER_PORT = 8943
LIVESERVER_TIMEOUT = 10
