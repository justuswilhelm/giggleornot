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

    def test_does_not_block_browser(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_block_amaze(self):
        response = self.app.get('/?ref=amaze')
        self.assertEqual(response.status_code, 403)

    def test_block_seo_spam(self):
        response = self.app.get('/', environ_base={
            'HTTP_REFERER': 'http://best-seo-report.com/'})
        self.assertEqual(response.status_code, 403)
