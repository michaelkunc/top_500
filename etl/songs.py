import requests
import collections
import os

Api = collections.namedtuple('Api', 'url data params')

last_fm = Api(url='http://ws.audioscrobbler.com//2.0/', data=None, params={'api_key': os.environ['LAST_FM_KEY'], 'format': 'json',
                                                                           'limit': '1', 'method': 'user.gettopartists', 'user': os.environ['LAST_FM_USER']})
MUSIKKI_BASE_URL = 'https://music-api.musikki.com/v1/'


def last_fm_top_artists():
    response = requests.get(url=last_fm.url, params=last_fm.params)
    return [{i['mbid']:[i['name'], i['playcount']]} for i in response.json()['topartists']['artist']]


def musikki_mkid(foreign_id):
    url = '{3}artists/?q=[foreign-id:{0}],[foreign-service:]&appkey={1}&appid={2}'.format(
        foreign_id, os.environ['MUSIKKI_APPKEY'], os.environ['MUSIKKI_APPID'], MUSIKKI_BASE_URL)
    response = requests.get(url)
    return response.json()['results'][0]['mkid']


def get_releases(mkid):
    url = '{3}artists/{0}/releases?q=[release-type:album],[release-subtype:Studio]&appkey={1}&appid={2}'.format(mkid,
                                                                                                                os.environ['MUSIKKI_APPKEY'], os.environ['MUSIKKI_APPID'], MUSIKKI_BASE_URL)
    response = requests.get(url)
    return [[i['mkid'], i['title']] for i in response.json()['results']]


def get_reviews(album_mkid):
    url = '{3}releases/{0}/reviews?&appkey={1}&appid={2}'.format(album_mkid,
                                                                 os.environ['MUSIKKI_APPKEY'], os.environ['MUSIKKI_APPID'], MUSIKKI_BASE_URL)
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


# def get_all_reviews(album_mkids):
#     return [get_reviews(i) for i in album_mkids]


# def get_all_album_scores(value_scales):
#     return [[album_score(i)] for i in value_scales]
