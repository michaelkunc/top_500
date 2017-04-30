import requests
import os
from flask_pymongo import MongoClient


class Artists(object):
    URL = 'http://ws.audioscrobbler.com//2.0/'

    def __init__(self, number_of_artists):
        self.params = {'api_key': os.environ['LFM_KEY'], 'format': 'json',
                       'limit': number_of_artists, 'method': 'user.gettopartists', 'user': os.environ['LFM_USER']}

    @property
    def artists_playcounts(self):
        response = requests.get(url=Artists.URL, params=self.params)
        return [[i['mbid'], i['name'], i['playcount']] for i in response.json()['topartists']['artist']]


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
        return [i['mkid'] for i in response.json()['results']]

    @property
    def reviews(self):
        reviews = []
        for r in self.releases:
            url = '{0}releases/{1}/reviews?{2}'.format(
                Reviews.URL_START, r, Reviews.URL_END)
            response = requests.get(url)
            reviews.append([i['rating'] for i in response.json()['results']])
        return [review for album in reviews for review in album]

    @property
    def average_score(self):
        normalized_scores = []
        try:
            for i in filter(None, self.reviews):
                if i['scale'] == 5:
                    normalized_scores.append(i['value'] * 2)
                elif i['scale'] == 0:
                    pass
                else:
                    normalized_scores.append(i['value'])
            return round(sum(normalized_scores) / float(len(normalized_scores)),
                         2)
        except ZeroDivisionError:
            return 'No Reviews'


def load_data_to_mongo(number_of_artists, db, collection):

    client = MongoClient('localhost', 27017)
    db = client[db]
    collection = db[collection]

    artist = Artists(number_of_artists)
    for a in artist.artists_playcounts:
        try:
            reviews = Reviews(a[0])
            artist_id, artist, playcount, avg_score, releases = a[
                0], a[1], a[2], reviews.average_score, reviews.releases
            key = {'_id': artist_id}
            data = {'artist_name': artist, 'playcount': playcount,
                    'average_score': avg_score, 'releases': releases}
            collection.replace_one(key, data, True)
            print('{0} was loaded to MongoDB!'.format(data))
        except IndexError:
            print('{0} could not be loaded to the db'.format(a))

# load_data_to_mongo(500, 'top_500', 'artists')


class ArtistIncr(object):

    def __init__(self, number_of_artists, db, collection):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[db]
        self.collection = collection
        self.artists = Artists(number_of_artists)

# incr = ArtistIncr(500, 'top_500', 'artists')

# print(incr.artists.artists_playcounts)
