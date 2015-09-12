from unittest import TestCase

from .. import app


class FlaskTestClientProxy(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['REMOTE_ADDR'] = environ.get('REMOTE_ADDR', '127.0.0.1')
        environ['HTTP_USER_AGENT'] = environ.get('HTTP_USER_AGENT', 'Chrome')
        return self.app(environ, start_response)


class IsHumanTestCase(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.wsgi_app = FlaskTestClientProxy(app.wsgi_app)
        self.app = app.test_client()

    def test_browser_receives_cookid(self):
        response = self.app.get('/')
        self.assertNotEqual(response.headers.getlist('Set-Cookie'), [])

    def test_amaze_receives_no_cookie(self):
        response = self.app.get('/?ref=amaze', environ_base={
            'HTTP_REFERER': 'http://www.twogifs.com/?ref=amaze'})
        self.assertEqual(response.headers.getlist('Set-Cookie'), [])

    def test_seo_spam_receives_no_cookie(self):
        response = self.app.get('/', environ_base={
            'HTTP_REFERER': 'http://best-seo-report.com'})
        self.assertEqual(response.headers.getlist('Set-Cookie'), [])
