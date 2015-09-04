from operator import itemgetter
from random import sample

from images import get_images
from gon import app


@app.cache.cached(key_prefix='get_image_ranking', timeout=10)
def get_image_ranking():
    return sorted(
        list(map(lambda x: (x[0].decode(), int(x[1])),
                 app.db.hgetall('images').items())),
        reverse=True, key=itemgetter(1))


def get_image_sample(count=2):
    images = get_images()
    return list(
        map(images.__getitem__, sample(range(0, len(images) - 1), count)))


# Image model
def image_score(image_id):
    if image_id in app.db.hgetall('images'):
        return app.db.hget('images', image_id)
    return 0


def upvote_image(image_id):
    app.db.hincrby('images', image_id, 1)


def downvote_image(image_id):
    app.db.hincrby('images', image_id, -1)
