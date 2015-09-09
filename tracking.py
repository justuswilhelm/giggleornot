"""Anonymous tracking! Yay!"""
from os import getenv
from multiprocessing import Pool

from flask import session
from mixpanel import Mixpanel

mp = Mixpanel(getenv('MIXPANEL_TOKEN'))
pool = Pool(2)


user_id = lambda: session.get('uid', 'anon')


def track_vote(image_id, is_up):
    pool.apply_async(mp.track, [user_id(), 'vote', {'image_id': image_id}])


def track_request(page, **extra):
    extra.update({'page': page})
    pool.apply_async(mp.track, [user_id(), 'request', extra])
