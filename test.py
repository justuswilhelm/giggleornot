from unittest import TestCase
from unittest.mock import MagicMock

from gon import ImageRanking


class ImageRankingTestCase(TestCase):
    def setUp(self):
        self.ir = ImageRanking()
        self.ir.image_retriever = MagicMock()

    def test_filter_images(self):
        up = MagicMock()
        up.id = 'up'
        down = MagicMock()
        down.id = 'down'
        self.ir.image_retriever.get_images.return_value = [up, down]
        self.ir.upvote_image('up', 10)
        self.ir.downvote_image('down', -10)
        self.assertEqual(self.ir.get_image_sample(), [up])
