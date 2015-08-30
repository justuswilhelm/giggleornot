"""Main module."""
from os import (
    environ,
    getenv,
)
from time import time
from random import sample

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

from images import get_images


# Configuration
app = Flask(__name__)
app.secret_key = environ['SECRET_KEY']
app.config.USERSNAP_KEY = environ['USERSNAP_KEY']
app.config.GA_ID = environ['GA_ID']

app_signals = Namespace()
voted = app_signals.signal('voted')

db = Redis.from_url(getenv('REDIS_URL', 'redis://localhost:6379/'))
db_get = lambda image_id: int(db['images:' + image_id]) if (
    'images:' + image_id) in db else db.set('images:' + image_id, 0) and 0
db_incr = lambda image_id: db.incr('images:' + image_id)

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
    return render_template(
        'index.html',
        image_a=image_a,
        image_b=image_b,
        image_a_score=db_get(image_a.id),
        image_b_score=db_get(image_b.id),
    )


@app.route("/vote")
def vote():
    yay = request.args['yay']
    db_incr(yay)
    voted.send(current_app._get_current_object(), image=yay)
    return redirect('/')


# Signal handlers
@request_finished.connect_via(app)
def log_pageview(sender, response, **extra):
    add_event("request", {"path": request.path})


@voted.connect_via(app)
def log_vote(sender, **extra):
    add_event("vote", {"id": extra['image']})


if __name__ == "__main__":
    app.run(debug=True)
