from os import environ
from time import time
from random import randint

from flask import (
    Flask,
    flash,
    render_template,
    redirect,
)

from images import get_images

app = Flask(__name__)
app.secret_key = environ['SECRET_KEY']


@app.route("/")
def index():
    """
    Index.

    Retriggers cache for image retrieval once every 60 hours
    """
    cache_var = lambda: int(time() / 3600)
    images = list(get_images(cache_var()))
    return render_template(
        'index.html',
        image_a=images.pop(randint(0, len(images))),
        image_b=images.pop(randint(0, len(images))),
    )


@app.route("/vote")
def vote():
    flash('Thank you for voting!')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
