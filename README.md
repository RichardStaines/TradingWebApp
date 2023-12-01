# TradingWebApp
A WebApp for tracking my trades and dividends.

I have provided a local SQLite db with some a TEST portfolio, some instruments and insrtrument prices loaded.
(1 step better than empty)

install-app.bat will get the packages needed.

run-app.bat will run the app

Load the folowing url in your web-browser
http://127.0.0.1:8000/

You can move the trading.sqlite file to another location and change the DATABASES.NAME setting in settings.py
e.g. move it to my Shared OneDrive location so I can get to it from my laptop or desktop
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'C:/Users/richa/OneDrive/Investments/trading.sqlite',
        # 'NAME': BASE_DIR / 'trading.sqlite',
    }
