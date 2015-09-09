"""Main module."""
from os import (
    environ,
    getenv,
)

from flask import Flask
from flask.ext.cache import Cache
from redis import Redis

app = Flask(__name__)

DEBUG = 'DEBUG' in environ
GA_ID = getenv('GA_ID')
OPTIMIZELY_KEY = getenv('OPTIMIZELY_KEY')
app.config.from_object(__name__)

app.db = Redis.from_url(
    getenv('REDIS_URL', 'redis://localhost:6379/'))
app.secret_key = environ['SECRET_KEY']


cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': getenv('REDIS_URL', 'redis://localhost:6379/'),
})

from . import views  # noqa
