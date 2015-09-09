web: newrelic-admin run-program gunicorn -b "0.0.0.0:$PORT" -w 3 gon:app --log-config gunicorn_logging.ini
redis: redis-server
