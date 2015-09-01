from functools import lru_cache
from operator import itemgetter
from random import sample
from time import time

from flask import current_app

from images import get_images


cache_var = lambda: int(time() / 600)


def get_image_ranking():
    current_app.logger.info(
        "Retrieving image ranking %s", _get_image_ranking.cache_info())
    return _get_image_ranking(cache_var())


@lru_cache()
def _get_image_ranking(time):
    return sorted(
        list(map(lambda x: (x[0].decode(), int(x[1])),
                 current_app.db.hgetall('images').items())),
        reverse=True, key=itemgetter(1))


def get_image_sample(count=2):
    images = get_images(cache_var())
    return map(images.__getitem__, sample(range(0, len(images) - 1), 2))


# Image model
db_get = lambda image_id: int(current_app.db.hget('images', image_id) or 0)
db_incr = lambda image_id: current_app.db.hincrby('images', image_id, 1)
