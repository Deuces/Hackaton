import os

basedir = os.path.abspath(os.path.dirname(__file__))

OPENID_PROVIDERS = [
    {'name': 'google', 'url': 'https://www.google.com/accounts/o8/id'}
]

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'secret_key'