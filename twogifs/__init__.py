"""Main module."""
from os import (
    environ,
    getenv,
)

from flask import Flask
from redis import Redis

app = Flask(__name__)

DEBUG = 'DEBUG' in environ
GA_ID = getenv('GA_ID')
app.config.from_object(__name__)

app.db = Redis.from_url(
    getenv('REDIS_URL', 'redis://localhost:6379/'))
app.secret_key = environ['SECRET_KEY']

from . import views  # noqa
