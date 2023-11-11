import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    basedir = os.path.dirname(os.path.dirname(__file__))
    weather_url = os.environ.get('WEATHER_URL')
    weather_key = os.environ.get('WEATHER_KEY')
    bot = os.environ.get('BOT')
    constructor = os.environ.get('CONSTRUCTOR')
    homepage = os.environ.get('HOMEPAGE')
    contact = os.environ.get('CONTACT')
    age = os.environ.get('AGE')
