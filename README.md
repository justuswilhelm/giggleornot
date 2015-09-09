# Giggle Or Not?
Rate and compare Imgur pictures a la Hot Or Not.

## Quick Start
```
pip install -r requirements.txt
cp .env.template .env
vim .env  # Add env vars (see Environment Variables)
foreman start
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
- `OPTIMIZELY_KEY` ... Optimizely Key
- `SECRET_KEY` ... set it to something secret.
