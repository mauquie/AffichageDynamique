from AffichageDynamique.settings import *

DEBUG = False
ALLOWED_HOSTS = ["127.0.0.0", "*"]

INSTALLED_APPS += (
    'gunicorn',
)
