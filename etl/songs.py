# from etl import credentials
import requests
import collections
import os

Api = collections.namedtuple('Api', 'url data params')

last_fm = Api(url='http://ws.audioscrobbler.com//2.0/', data=None, params={'api_key': os.environ['LAST_FM_KEY'], 'format': 'json',
                                                                           'limit': '1', 'method': 'user.gettopartists', 'user': os.environ['LAST_FM_USER']})


def last_fm_top_artists():
    response = requests.get(url=last_fm.url, params=last_fm.params)
    return [{i['mbid']:[i['name'], i['playcount']]} for i in response.json()['topartists']['artist']]


def musikki_mkid(foreign_id):
    url = 'https://music-api.musikki.com/v1/artists/?q=[foreign-id:{0}],[foreign-service:]&appkey={1}&appid={2}'.format(
        foreign_id, os.environ['MUSIKKI_APPKEY'], os.environ['MUSIKKI_APPID'])
    response = requests.get(url)
    return response.json()['results'][0]['mkid']


def get_releases(mkid):
    url = 'https://music-api.musikki.com/v1/artists/100094349/releases?q=[release-type:album],[release-subtype:Studio]&appkey={0}&appid={1}'.format(
        os.environ['MUSIKKI_APPKEY'], os.environ['MUSIKKI_APPID'])
    response = requests.get(url)
    return [[i['mkid'], i['title']] for i in response.json()['results']]


def get_reviews(album_mkid):
    url = 'https://music-api.musikki.com/v1/releases/101252510/reviews?&appkey={0}&appid={1}'.format(
        os.environ['MUSIKKI_APPKEY'], os.environ['MUSIKKI_APPID'])
    response = requests.get(url)
    return [i['rating'] for i in response.json()['results']]


def album_score(value_scale):
    normalized_scores = []
    for i in value_scale:
        if i['scale'] == 5:
            normalized_scores.append(i['value'] * 2)
        elif i['scale'] == 0:
            pass
        else:
            normalized_scores.append(i['value'])
    return round(sum(normalized_scores) / float(len(normalized_scores)), 2)
