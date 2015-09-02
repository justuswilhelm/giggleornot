from logging import getLogger
from functools import reduce
from operator import add
from os import getenv

from imgurpython import ImgurClient
from imgurpython.imgur.models.gallery_image import GalleryImage

from gon import app

logger = getLogger(__name__)
client = ImgurClient(
    getenv('IMGUR_CLIENT_ID'), getenv('IMGUR_CLIENT_SECRET'))


# Example request
@app.cache.cached(timeout=300)
def get_images():
    """
    Get animated images from imgur.

    Caches 60 different versions.
    """
    return list(filter(
        lambda item: item.animated, filter(
            lambda item: isinstance(item, GalleryImage),
            reduce(add, (client.gallery(page=i) for i in range(10)))
        ))
    )


if __name__ == "__main__":
    for i in get_images():
        print(i.link)
