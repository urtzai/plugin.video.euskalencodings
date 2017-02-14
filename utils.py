import requests

API_URL = 'http://torretxea.ddns.net/api/v1/kodi'


def get_categories():
    data = requests.get(API_URL)
    return data.json()


def get_contents(url):
    data = requests.get(url)
    return data.json()


def get_qualities(url):
    data = requests.get(url)
    return data.json()


def get_torrents(url):
    data = requests.get(url)
    return data.json()
