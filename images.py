from logging import getLogger
from functools import reduce
from operator import add
from os import getenv

from imgurpython import ImgurClient
from imgurpython.imgur.models.gallery_image import GalleryImage

from gon import app

TIMEOUT = 60 * 15

logger = getLogger(__name__)
client = ImgurClient(
    getenv('IMGUR_CLIENT_ID'), getenv('IMGUR_CLIENT_SECRET'))
gallery = app.cache.memoize(timeout=TIMEOUT)(
    lambda page: client.gallery(page=page))


# Example request
@app.cache.cached(key_prefix='get_images', timeout=TIMEOUT)
def get_images():
    """
    Get animated images from imgur.

    Caches 60 different versions.
    """
    return list(filter(
        lambda item: item.animated, filter(
            lambda item: isinstance(item, GalleryImage),
            reduce(add, (gallery(i) for i in range(10)))
        ))
    )
