"""Main module."""
from logging import (
    INFO,
    Formatter,
    StreamHandler,
)
from operator import itemgetter
from os import (
    environ,
    getenv,
)
from random import sample
from time import time

from blinker import Namespace
from flask import (
    current_app,
    Flask,
    render_template,
    redirect,
    request,
    request_finished,
    send_from_directory,
)
from keen.client import KeenClient
from keen import add_event
from redis import Redis
from rq.decorators import job

from images import get_images

__version__ = "Unreleased"


# Configuration
app = Flask(__name__)
app.debug = 'DEBUG' in environ
app.secret_key = environ['SECRET_KEY']
app.config.USERSNAP_KEY = environ['USERSNAP_KEY']
app.config.GA_ID = environ['GA_ID']

app_signals = Namespace()
voted = app_signals.signal('voted')

# Redis
db = Redis.from_url(getenv('REDIS_URL', 'redis://localhost:6379/'))

# Image model
db_get = lambda image_id: int(db.hget('images', image_id) or 0)
db_incr = lambda image_id: db.hincrby('images', image_id, 1)

# RQ
add_event = job('default', connection=db)(add_event)

keen_client = KeenClient(
    master_key=environ['KEEN_MASTER_KEY'],
    project_id=environ['KEEN_PROJECT_ID'],
    read_key=environ['KEEN_READ_KEY'],
    write_key=environ['KEEN_WRITE_KEY'],
)


# Views
@app.route('/robots.txt')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route("/")
def index():
    """
    Index.

    Retriggers cache for image retrieval once every 10 minutes
    """
    cache_var = int(time() / 600)
    images = get_images(cache_var)
    # Get two random images
    image_a, image_b = map(
        images.__getitem__, sample(range(0, len(images) - 1), 2))
    image_a.score = db_get(image_a.id)
    image_b.score = db_get(image_b.id)
    return render_template(
        'index.html',
        image_a=image_a,
        image_b=image_b,
    )


@app.route("/vote")
def vote():
    yay = request.args['yay']
    db_incr(yay)
    current_app.logger.info("Voting for %s. New Score is %d", yay, db_get(yay))
    voted.send(current_app._get_current_object(), image=yay)
    return redirect('/')


@app.route("/top")
def show_top():
    images = list(
        map(lambda x: (x[0].decode(), int(x[1])),
            db.hgetall('images').items()))
    images_sorted = sorted(images, key=itemgetter(1))[:10]
    return render_template('top.html', images=images_sorted)


@app.errorhandler(500)
@app.errorhandler(404)
def http_error_handler(error):
    return redirect("/")


@app.before_request
def before_request():
    if request.url.startswith('https://'):
        url = request.url.replace('https://', 'http://', 1)
        code = 301
        return redirect(url, code=code)


# Signal handlers
@request_finished.connect_via(app)
def log_pageview(sender, response, **extra):
    add_event.delay("request", {"path": request.path})


@voted.connect_via(app)
def log_vote(sender, **extra):
    add_event.delay("vote", {"id": extra['image']})


if __name__ == "__main__":
    app.run(debug=True)
