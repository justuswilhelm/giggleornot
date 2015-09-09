from uuid import uuid4

from flask import (
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

image_ranking = ImageRanking()


# Views
@app.route('/robots.txt')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route("/")
def index():
    if {'yay', 'nay'}.issubset(request.args.keys()):
        yay = request.args['yay']
        nay = request.args['nay']
        key = '{}:{}'.format(request.access_route, sorted((yay, nay)))

        if key not in app.db:
            image_ranking.upvote_image(yay)
            image_ranking.downvote_image(nay)
            track_vote(yay, nay)
            pipe = app.db.pipeline()
            pipe.set(key, '')
            pipe.expire(key, 30)
            pipe.execute()
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


@app.before_request
def check_session():
    if 'uid' not in session and request.method != 'HEAD':
        session.permanent = True
        session['uid'] = str(uuid4())
        track_new_user()
