from operator import itemgetter
from random import sample

from images import get_images
from gon import app


@app.cache.cached(timeout=30)
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
db_get = lambda image_id: int(app.db.hget('images', image_id) or 0)
db_incr = lambda image_id: app.db.hincrby('images', image_id, 1)
