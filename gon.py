from os import (
    environ,
    getenv,
)
from time import time
from random import sample

from flask import (
    Flask,
    flash,
    render_template,
    redirect,
    request,
)

from images import get_images

from redis import Redis

app = Flask(__name__)
app.secret_key = environ['SECRET_KEY']

db = Redis.from_url(getenv('REDIS_URL', 'redis://localhost:6379/'))
db_get = lambda image_id: int(db['images:' + image_id]) if (
    'images:' + image_id) in db else db.set('images:' + image_id, 0) and 0
db_incr = lambda image_id: db.incr('images:' + image_id)


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
    nay = request.args['nay']
    better_image = max(yay, nay, key=lambda img: db_get(img))
    if db_get(better_image) == 0:
        flash('Thank you for voting!')
    elif better_image == yay:
        flash('Thank you for voting! Others agree with you!')
    else:
        flash('Thank you for voting for the unpopular opinion!')
    print(better_image)
    db_incr(yay)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
