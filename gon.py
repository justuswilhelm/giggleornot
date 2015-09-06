"""Main module."""
from os import (
    environ,
    getenv,
)

from flask import Flask
from flask.ext.cache import Cache

__version__ = "Unreleased"


# Configuration
app = Flask(__name__)
app.debug = 'DEBUG' in environ
app.secret_key = environ['SECRET_KEY']
app.config.GA_ID = getenv('GA_ID')
app.config.OPTIMIZELY_KEY = getenv('OPTIMIZELY_KEY')
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': getenv('REDIS_URL', 'redis://localhost:6379/'),
})

from data import ImageRanking
import views  # noqa

app.image_ranking = ImageRanking()
if __name__ == "__main__":
    app.run(debug=True)
