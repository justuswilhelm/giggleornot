from logging import getLogger
from functools import reduce
from pickle import (
    dumps,
    loads,
)
from operator import add
from os import getenv

from imgurpython import ImgurClient
from imgurpython.imgur.models.gallery_image import GalleryImage

from . import app


class ImageRetriever:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.client = ImgurClient(
            getenv('IMGUR_CLIENT_ID'), getenv('IMGUR_CLIENT_SECRET'))

    def retrieve_images(self, no_pages=10):
        images = filter(
            lambda item: isinstance(item, GalleryImage) and item.animated,
            reduce(add, (self.client.gallery(page=i) for i in range(no_pages)))
        )
        pipe = app.db.pipeline()
        pipe.delete('images')
        for image in images:
            pipe.hsetnx('images', image.id, dumps(image))
        pipe.execute()

    def get_images(self):
        return list(map(loads, app.db.hvals('images')))

    def get_image(self, image_id):
        return loads(app.db.hget('images', image_id))
