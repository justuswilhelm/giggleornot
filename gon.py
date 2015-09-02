"""Main module."""
from os import (
    environ,
    getenv,
)

from flask import (
    current_app,
    Flask,
    render_template,
    redirect,
    request,
    send_from_directory,
)
from flask.ext.cache import Cache
from redis import Redis

__version__ = "Unreleased"


# Configuration
app = Flask(__name__)
app.debug = 'DEBUG' in environ
app.secret_key = environ['SECRET_KEY']
app.config.USERSNAP_KEY = environ['USERSNAP_KEY']
app.config.GA_ID = environ['GA_ID']

# Redis
app.cache = Cache(
    app, config={
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': getenv('REDIS_URL', 'redis://localhost:6379/'),
    })
app.db = Redis.from_url(getenv('REDIS_URL', 'redis://localhost:6379/'))

from data import (
    get_image_sample,
    get_image_ranking,
    db_get,
    db_incr,
)


# Views
@app.route('/robots.txt')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route("/")
def index():
    # Get two random images
    images = get_image_sample()
    [setattr(image, 'score', db_get(image.id)) for image in images]
    return render_template(
        'index.html',
        images=images,
        ranking=get_image_ranking()[:5],
    )


@app.route("/vote")
def vote():
    image = request.args['image']
    db_incr(image)
    current_app.logger.info(
        "Voting for %s. New Score is %d", image, db_get(image))
    return redirect('/?ref=vote')


@app.errorhandler(500)
@app.errorhandler(404)
def http_error_handler(error):
    return redirect("/?ref=error")


# Signal handlers
@app.before_request
def log_pageview():
    current_app.logger.info(
        "REMOTE_ADDR %s User Agent %s",
        request.remote_addr,
        request.user_agent.string,
    )


if __name__ == "__main__":
    app.run(debug=True)
