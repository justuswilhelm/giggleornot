# Giggle Or Not?
Rate and compare Imgur pictures a la Hot Or Not.

## Quick Start
```
pip install -r requirements.txt
cp .env.template .env
vim .env  # Add env vars (see Environment Variables)
redis-server &
foreman run ./manage.py runserver
```

## Requirements
- `gem install foreman`
- `pip install -r requirements.txt`

## Environment Variables
Should reside in `.env` so that foreman can pick them up.

- `GA_ID` ... Google Analytics ID
- `IMGUR_CLIENT_ID` and `IMGUR_CLIENT_SECRET` ... can be retrieved in your app
  settings on https://api.imgur.com.
- `MIXPANEL_TOKEN` ... Mixpanel Project Token
- `SECRET_KEY` ... set it to something secret.

## How to retrieve new images from imgur
```
./manage.py retrieve_images
```

## How to purge scores for invalid GIF ids
Often, GIFs get pushed off the imgur front page after some time. GIFs that
appear in the ranking can then become invalid. In order to remove scores for old
GIFs, run
```
./manage.py remove_invalid_scores
```
