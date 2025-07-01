import os

from dotenv import load_dotenv


def load_info():
    load_dotenv()
    _host = os.getenv('PVE_HOST')
    _user = os.getenv('PVE_USER')
    _pass = os.getenv('PVE_PASSWORD')
    return _host, _user, _pass