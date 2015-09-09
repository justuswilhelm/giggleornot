from uuid import uuid4

from flask import (
    current_app,
    request,
    send_from_directory,
    session,
    render_template,
    redirect,
)
from imgurpython.helpers.error import ImgurClientError

from gon import app

from tracking import (
    track_vote,
    track_page_view,
)


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
        current_app.image_ranking.upvote_image(yay)
        current_app.image_ranking.downvote_image(nay)
        track_vote(yay, is_up=True)
        track_vote(yay, is_up=False)

    # Get two random images
    try:
        images = current_app.image_ranking.get_image_sample()
    except ImgurClientError:
        return redirect('/?ref=imgur-client-error')

    return render_template(
        'index.html',
        images=images,
        ranking=current_app.image_ranking.get_image_ranking()[:5],
    )


@app.route("/<left>")
def compare_one(left):
    images = [current_app.image_ranking.get_image_with_score(
        left)] + current_app.image_ranking.get_image_sample(1)
    return render_template(
        'index.html',
        images=images,
        ranking=current_app.image_ranking.get_image_ranking()[:5],
    )


@app.route("/<left>/<right>")
def compare_two(left, right):
    images = [
        current_app.image_ranking.get_image_with_score(left),
        current_app.image_ranking.get_image_with_score(right),
    ]
    return render_template(
        'index.html',
        images=images,
        ranking=current_app.image_ranking.get_image_ranking()[:5],
    )


@app.route("/ranking")
def ranking():
    return render_template(
        'ranking.html',
        ranking=current_app.image_ranking.get_image_ranking(),
    )


@app.before_request
def check_session():
    if 'uid' not in session:
        session.permanent = True
        session['uid'] = str(uuid4())


@app.after_request
def page_view(response):
    track_page_view(request.path, **request.args)
    return response
