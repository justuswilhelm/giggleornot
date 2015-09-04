from os import getenv
from random import shuffle

from redis import Redis

from images import ImageRetriever


class ImageRanking:

    UPVOTE = 1
    DOWNVOTE = -1
    MIN_SCORE = 0
    KEY_NAME = 'image_scores'

    def __init__(self):
        self.db = Redis.from_url(
            getenv('REDIS_URL', 'redis://localhost:6379/'))
        self.image_retriever = ImageRetriever()

    def filter_images(self, min_score=MIN_SCORE):
        images = self.image_retriever.get_images(1)
        scores = dict(self.get_scores())
        for i in images:
            i.score = scores.get(i.id, 0)
        return filter(lambda i: i.score >= min_score, images)

    def get_scores(self):
        return ((e[0].decode(), e[1]) for e in self.db.zrange(
            self.KEY_NAME, 0, -1, withscores=True, score_cast_func=int))

    def get_image_ranking(self):
        return [(e[0].decode(), e[1]) for e in self.db.zrevrangebyscore(
            self.KEY_NAME, 'inf', 0, withscores=True, score_cast_func=int)]

    def get_image_sample(self, count=2):
        images = list(self.filter_images())
        shuffle(images)
        return images[:count]

    def image_score(self, image_id):
        return self.db.zscore(self.KEY_NAME, image_id) or 0

    def upvote_image(self, image_id, score=UPVOTE):
        self.db.zincrby(self.KEY_NAME, image_id, score)

    def downvote_image(self, image_id, score=DOWNVOTE):
        self.db.zincrby(self.KEY_NAME, image_id, -abs(score))
