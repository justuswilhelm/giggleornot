"""Anonymous tracking! Yay!"""
from os import getenv
from multiprocessing import Pool

from mixpanel import Mixpanel

mp = Mixpanel(getenv('MIXPANEL_TOKEN'))
pool = Pool(2)


def track_vote(image_id, is_up):
    pool.apply_async(mp.track, ['anon', 'vote', {'image_id': image_id}])


def track_page_view(page, **extra):
    extra.update({'page': page})
    pool.apply_async(mp.track, ['anon', 'page_view', extra])
