web: newrelic-admin run-program gunicorn -b "0.0.0.0:$PORT" -w 3 gon:app --log-config gunicorn_logging.ini
worker: newrelic-admin run-program python -u run-worker.py
redis: redis-server --save ""
