from . import app

referrer_blacklist = [
    'http://best-seo-report.com',
    'http://www.twogifs.com/?ref=amaze',
]
is_human = lambda request: all([
    request.method != 'HEAD',
    request.user_agent.browser is not None,
    request.referrer not in referrer_blacklist,
    not is_crawler(request),
    request.path != '/ping',
])
# http://werkzeug.pocoo.org/docs/0.10/utils/#module-werkzeug.useragents
is_crawler = lambda request: request.user_agent.browser in [
    'google', 'yahoo', 'aol', 'ask']

has_valid_session = lambda session: 'uid' in session

rate_limit_key = lambda session, key: '{}:{}'.format(session['uid'], key)


def rate_limit(session, raw_key):
    key = rate_limit_key(session, raw_key)

    pipe = app.db.pipeline()
    pipe.set(key, '')
    pipe.expire(key, 30)
    pipe.execute()


is_rate_limited = lambda session, raw_key: rate_limit_key(
    session, raw_key) in app.db
