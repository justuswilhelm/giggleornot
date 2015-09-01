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
from redis import Redis

from data import (
    get_image_sample,
    get_image_ranking,
    db_get,
    db_incr,
)

__version__ = "Unreleased"


# Configuration
app = Flask(__name__)
app.debug = 'DEBUG' in environ
app.secret_key = environ['SECRET_KEY']
app.config.USERSNAP_KEY = environ['USERSNAP_KEY']
app.config.GA_ID = environ['GA_ID']

# Redis
app.db = Redis.from_url(getenv('REDIS_URL', 'redis://localhost:6379/'))


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
    # Get two random images
    image_a, image_b = get_image_sample()
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
    return redirect('/?ref=vote')


@app.route("/top")
def show_top():
    return render_template('top.html', images=get_image_ranking()[:10])


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
