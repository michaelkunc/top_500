import requests
import os


REVIEWS_URL = 'https://music-api.musikki.com/v1/'


class Artists(object):
    URL = 'http://ws.audioscrobbler.com//2.0/'

    def __init__(self, number_of_artists):
        self.params = {'api_key': os.environ['LFM_KEY'], 'format': 'json',
                       'limit': number_of_artists, 'method': 'user.gettopartists', 'user': os.environ['LFM_USER']}

    @property
    def artists_playcounts(self):
        response = requests.get(url=Artists.URL, params=self.params)
        return [{i['mbid']:[i['name'], i['playcount']]} for i in response.json()['topartists']['artist']]


class Reviews(object):
    URL_START = 'https://music-api.musikki.com/v1/'
    URL_END = '&appkey={0}&appid={1}'.format(
        os.environ['KEY'], os.environ['ID'])

    def __init__(self, foreign_artist_id):
        self.foreign_id = foreign_artist_id

    @property
    def mkid(self):
        url = '{0}artists/?q=[foreign-id:{1}],[foreign-service:]{2}'.format(
            Reviews.URL_START, self.foreign_id, Reviews.URL_END)
        response = requests.get(url)
        return response.json()['results'][0]['mkid']

    @property
    def releases(self):
        url = '{0}artists/{1}/releases?q=[release-type:album],[release-subtype:Studio]{2}'.format(
            Reviews.URL_START, self.mkid, Reviews.URL_END)
        response = requests.get(url)
        return [[i['mkid'], i['title']] for i in response.json()['results']]


# Legacy Code Below


# def musikki_mkid(foreign_id):
#     url = '{3}artists/?q=[foreign-id:{0}],[foreign-service:]&appkey={1}&appid={2}'.format(
#         foreign_id, os.environ['KEY'], os.environ['ID'], REVIEWS_URL)
#     response = requests.get(url)
#     return response.json()['results'][0]['mkid']


def get_releases(mkid):
    url = '{3}artists/{0}/releases?q=[release-type:album],[release-subtype:Studio]&appkey={1}&appid={2}'.format(mkid,
                                                                                                                os.environ['KEY'], os.environ['ID'], REVIEWS_URL)
    response = requests.get(url)
    return [[i['mkid'], i['title']] for i in response.json()['results']]


def get_reviews(album_mkid):
    url = '{3}releases/{0}/reviews?&appkey={1}&appid={2}'.format(album_mkid,
                                                                 os.environ['KEY'], os.environ['ID'], REVIEWS_URL)
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


def get_all_reviews(album_mkids):
    return [get_reviews(i[0]) for i in album_mkids]


# def get_all_album_scores(value_scales):
#     return [[album_score(i)] for i in value_scales]
