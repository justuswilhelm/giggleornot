from logging import getLogger
from functools import reduce
from operator import add
from os import getenv

from imgurpython import ImgurClient
from imgurpython.imgur.models.gallery_image import GalleryImage

from gon import cache


class ImageRetriever:
    TIMEOUT = 60 * 30

    def __init__(self):
        self.logger = getLogger(__name__)
        self.client = ImgurClient(
            getenv('IMGUR_CLIENT_ID'), getenv('IMGUR_CLIENT_SECRET'))
        self.gallery = cache.memoize(timeout=self.TIMEOUT)(
            lambda page: self.client.gallery(page=page))


# Example request
    @cache.memoize(timeout=TIMEOUT)
    def get_images(self):
        """
        Get animated images from imgur.

        Caches 60 different versions.
        """
        return list(filter(
            lambda item: item.animated, filter(
                lambda item: isinstance(item, GalleryImage),
                reduce(add, (self.gallery(i) for i in range(10)))
            ))
        )
