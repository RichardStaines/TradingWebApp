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

Setting up reference data.

1. setup your portfolios. e.g. myISA or myPension 
2. setup the instruments you trade or want to monitor
3. Use the Load prices button, check the prices update
4. Scrape for dividend schedules
5. Enter your Positions
6. Enter your dividends
7. Enter trades - note these will affect your positions

There is an option to load Cash, dividends and positions from a csv file. The format expected is a dump csv from Interactive Investor. 
This load does not affect the positions and bypasses PnL calcs.

There is an option for laoding positions from csv. This is also Interactive Inverstor format. 
