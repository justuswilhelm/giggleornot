from random import shuffle

from . import app
from .images import ImageRetriever


class ImageRanking:

    UPVOTE = 1
    DOWNVOTE = -0.5
    MIN_SCORE = -5
    KEY_NAME = 'image_scores'

    def __init__(self):
        self.image_retriever = ImageRetriever()

    def filter_images(self, min_score=MIN_SCORE):
        images = self.image_retriever.get_images()
        scores = self.get_scores()
        for i in images:
            i.score = scores.get(i.id, 0)

        return filter(lambda i: i.score > min_score, images)

    def get_scores(self):
        return dict((e[0].decode(), e[1]) for e in app.db.zrange(
            self.KEY_NAME, 0, -1, withscores=True))

    def get_image_with_score(self, image_id):
        try:
            img = self.image_retriever.get_image(image_id)
        except KeyError:
            img = self.get_image_sample(1)[0]

        img.score = self.image_score(image_id)
        return img

    def get_image_ranking(self):
        return [(e[0].decode(), e[1]) for e in app.db.zrevrangebyscore(
            self.KEY_NAME, 'inf', '-inf', withscores=True)]

    def remove_invalid_scores(self):
        for image_id in self.get_image_ranking():
            try:
                self.image_retriever.get_image(image_id)
            except KeyError:
                app.db.zrem(self.KEY_NAME, image_id)

    def get_image_sample(self, count=2):
        images = list(self.filter_images())
        shuffle(images)
        return images[:count]

    def image_score(self, image_id):
        return app.db.zscore(self.KEY_NAME, image_id) or 0

    def upvote_image(self, image_id, score=UPVOTE):
        app.db.zincrby(self.KEY_NAME, image_id, score)

    def downvote_image(self, image_id, score=DOWNVOTE):
        app.db.zincrby(self.KEY_NAME, image_id, -abs(score))
