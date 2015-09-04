from flask import (
    current_app,
    request,
    send_from_directory,
    render_template,
    redirect,
)
from imgurpython.helpers.error import ImgurClientError

from gon import app


# Views
@app.route('/robots.txt')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route("/")
def index():
    if {'yay', 'nay'}.issubset(request.args.keys()):
        current_app.image_ranking.upvote_image(request.args['yay'])
        current_app.image_ranking.downvote_image(request.args['nay'])

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
