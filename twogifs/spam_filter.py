from flask import (
    request,
    session,
)

from . import app

referrer_blacklist = [
    'http://best-seo-report.com',
    'http://www.twogifs.com/?ref=amaze',
]
is_human = lambda: all([
    request.method != 'HEAD',
    request.user_agent.browser is not None,
    request.args.get('ref', '') != 'amaze',
    request.referrer not in referrer_blacklist,
])
# http://werkzeug.pocoo.org/docs/0.10/utils/#module-werkzeug.useragents
is_crawler = lambda: request.user_agent.browser in [
    'google', 'yahoo', 'aol', 'ask']

has_valid_session = lambda: 'uid' in session

rate_limit_key = lambda key: '{}:{}'.format(request.access_route, key)


def rate_limit(key):
    pipe = app.db.pipeline()
    pipe.set(key, '')
    pipe.expire(key, 30)
    pipe.execute()


is_rate_limited = lambda key: rate_limit_key(key) in app.db
