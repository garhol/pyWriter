from pyWriter.lib.settings.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pywriter',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'password',                  # Not used with sqlite3.
    }
}

MEDIA_ROOT = '/home/john/python_projects/pyWriter/library-rename'
MEDIA_URL = 'http://127.0.0.1:8000/library/'
