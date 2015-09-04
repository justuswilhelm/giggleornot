from os import getenv
from random import sample

from redis import Redis

from images import ImageRetriever


class ImageRanking:

    UPVOTE = 1
    DOWNVOTE = -1
    KEY_NAME = 'image_scores'

    def __init__(self):
        self.db = Redis.from_url(
            getenv('REDIS_URL', 'redis://localhost:6379/'))
        self.image_retriever = ImageRetriever()

    def get_image_ranking(self):
        return [(e[0].decode(), e[1]) for e in self.db.zrevrangebyscore(
            self.KEY_NAME, 'inf', 0, withscores=True, score_cast_func=int)]

    def get_image_sample(self, count=2):
        images = self.image_retriever.get_images()
        return list(
            map(images.__getitem__, sample(range(0, len(images) - 1), count)))

    def image_score(self, image_id):
        return self.db.zscore(self.KEY_NAME, image_id) or 0

    def upvote_image(self, image_id):
        self.db.zincrby(self.KEY_NAME, image_id, self.UPVOTE)

    def downvote_image(self, image_id):
        self.db.zincrby(self.KEY_NAME, image_id, self.DOWNVOTE)
