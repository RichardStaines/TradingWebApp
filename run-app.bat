call .\venv\Scripts\activate.bat

start python manage.py runserver

rundll32 url.dll,FileProtocolHandler "http://127.0.0.1:8000/"

echo %cd%
start-react.bat


pause
