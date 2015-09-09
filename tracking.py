"""Anonymous tracking! Yay!"""
from os import getenv
from multiprocessing import Pool

from flask import (
    request,
    session,
)
from mixpanel import Mixpanel

mp = Mixpanel(getenv('MIXPANEL_TOKEN'))
pool = Pool(2)


user_id = lambda: session.get('uid', 'anon')


def track_vote(up, down):
    pool.apply_async(
        mp.track,
        [user_id(), 'vote', {'up': up, 'down': down}]
    )


def track_new_user():
    pool.apply_async(
        mp.track, [
            user_id(),
            'new_user',
            {'$browser': request.user_agent.browser,
             '$browser_version': request.user_agent.version,
             '$initial_referrer': request.args.get('ref') or request.referrer,
             },
        ])
    pool.apply_async(
        mp.people_set, [
            user_id(),
            {},
        ])
