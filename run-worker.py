from os import getenv

from redis import Redis
from rq import Worker, Queue, Connection
from rq.logutils import setup_loghandlers

listen = ['default']

conn = Redis.from_url(getenv('REDIS_URL', 'redis://localhost:6379/rq'))

with Connection(conn):
    worker = Worker(map(Queue, listen))
    setup_loghandlers(level='WARNING')
    worker.work()
