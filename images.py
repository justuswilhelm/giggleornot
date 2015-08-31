from logging import getLogger
from functools import lru_cache, reduce
from operator import add
from os import getenv
from imgurpython import ImgurClient
from imgurpython.imgur.models.gallery_image import GalleryImage

logger = getLogger(__name__)
client = ImgurClient(
    getenv('IMGUR_CLIENT_ID'), getenv('IMGUR_CLIENT_SECRET'))


# Example request
@lru_cache(maxsize=60)
def get_images(hour):
    """
    Get animated images from imgur.

    Caches 60 different versions.
    """
    logger.info("Retrieving new images, {}".format(get_images.cache_info()))
    return list(filter(
        lambda item: item.animated, filter(
            lambda item: isinstance(item, GalleryImage),
            reduce(add, (client.gallery(page=i) for i in range(10)))
        ))
    )


if __name__ == "__main__":
    for i in get_images():
        print(i.link)
