from flask import (
    request,
    session,
)

from . import app

referrer_blacklist = [
    'http://best-seo-report.com/',
    'http://www.twogifs.com/?ref=amaze',
]
is_human = lambda: (
    request.method != 'HEAD' and
    request.user_agent.browser is not None and
    request.args.get('ref', '') != 'amaze' and
    request.referrer not in referrer_blacklist,
)
has_valid_session = lambda: 'uid' in session

rate_limit_key = lambda key: '{}:{}'.format(request.access_route, key)


def rate_limit(key):
    pipe = app.db.pipeline()
    pipe.set(key, '')
    pipe.expire(key, 30)
    pipe.execute()


is_rate_limited = lambda key: rate_limit_key(key) not in app.db
