from uuid import uuid4

from flask import (
    abort,
    request,
    send_from_directory,
    session,
    render_template,
    redirect,
)
from imgurpython.helpers.error import ImgurClientError

from .data import ImageRanking
from . import app
from .tracking import (
    track_vote,
    track_new_user,
)
from .spam_filter import (
    is_human,
    has_valid_session,
    rate_limit,
    is_rate_limited,
)

image_ranking = ImageRanking()


# Views
@app.route('/robots.txt')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route("/")
def index():
    if {'yay', 'nay'}.issubset(request.args.keys()) and has_valid_session():
        yay = request.args['yay']
        nay = request.args['nay']
        key = sorted((yay, nay))

        if is_rate_limited(key):
            image_ranking.upvote_image(yay)
            image_ranking.downvote_image(nay)
            track_vote(yay, nay)
            rate_limit(key)
        else:
            app.logger.warning('Rate limiting for {}'.format(key))

    # Get two random images
    try:
        images = image_ranking.get_image_sample()
    except ImgurClientError:
        return redirect('/?ref=imgur-client-error')

    return render_template(
        'index.html',
        images=images,
        ranking=image_ranking.get_image_ranking()[:5],
    )


@app.route("/<left>")
def compare_one(left):
    images = [image_ranking.get_image_with_score(
        left)] + image_ranking.get_image_sample(1)
    return render_template(
        'index.html',
        images=images,
        ranking=image_ranking.get_image_ranking()[:5],
    )


@app.route("/<left>/<right>")
def compare_two(left, right):
    images = [
        image_ranking.get_image_with_score(left),
        image_ranking.get_image_with_score(right),
    ]
    return render_template(
        'index.html',
        images=images,
        ranking=image_ranking.get_image_ranking()[:5],
    )


@app.route("/ranking")
def ranking():
    return render_template(
        'ranking.html',
        ranking=image_ranking.get_image_ranking(),
    )


@app.route("/ping")
def ping():
    return "YESYES"


@app.before_request
def check_session():
    if not is_human():
        abort(403)
    if not has_valid_session():
        create_session()


def create_session():
    session.permanent = True
    session['uid'] = str(uuid4())
    track_new_user()
