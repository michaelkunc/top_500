from etl import credentials
import requests
import collections

Api = collections.namedtuple('Api', 'url data params')

last_fm = Api(url='http://ws.audioscrobbler.com//2.0/', data=None, params={'api_key': credentials.LAST_FM_KEY, 'format': 'json',
                                                                           'limit': '1', 'method': 'user.gettopartists', 'user': credentials.LAST_FM_USER})


def last_fm_top_artists():
    response = requests.get(url=last_fm.url, params=last_fm.params)
    return [{i['mbid']:[i['name'], i['playcount']]} for i in response.json()['topartists']['artist']]


def musikki_mkid(foreign_id):
    url = 'https://music-api.musikki.com/v1/artists/?q=[foreign-id:{0}],[foreign-service:]&appkey={1}&appid={2}'.format(
        foreign_id, credentials.MUSIKKI_APPKEY, credentials.MUSIKKI_APPID)
    response = requests.get(url)
    return response.json()['results'][0]['mkid']


def get_releases(mkid):
    url = 'https://music-api.musikki.com/v1/artists/100094349/releases?q=[release-type:album],[release-subtype:Studio]&appkey=4833d334c6b624fae1a5c35dbdd2f1aa&appid=9130e8b637ff1ecbe198740fd33c36df'
    response = requests.get(url)
    return [[i['mkid'], i['title']] for i in response.json()['results']]
