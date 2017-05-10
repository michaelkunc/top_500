import requests
import os
from flask_pymongo import MongoClient

MONGO = {'HOST': 'localhost', 'PORT': 27017,
         'db': 'top_500', 'collection': 'artists'}

CLIENT = MongoClient('localhost', 27017)
DB = CLIENT['top_500']
COLLECTION = DB['artists']


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


def load_data_to_mongo(number_of_artists):

    artist = Artists(number_of_artists)
    for a in artist.artists_playcounts:
        try:
            reviews = Reviews(a[0])
            artist_id, artist, playcount, avg_score, releases = a[
                0], a[1], a[2], reviews.average_score, reviews.releases
            key = {'_id': artist_id}
            data = {'artist_name': artist, 'playcount': playcount,
                    'average_score': avg_score, 'releases': releases}
            COLLECTION.replace_one(key, data, True)
            print('{0} was loaded to MongoDB!'.format(data))
        except IndexError:
            print('{0} could not be loaded to the db'.format(a))


class ArtistFull(object):

    def __init__(self, number_of_artists):
        self.artists = Artists(number_of_artists)

    def load_data(self):
        for a in self.artists.artists_playcounts:
            try:
                reviews = Reviews(a[0])
                artist_id, artist, playcount, avg_score, releases = a[
                    0], a[1], a[2], reviews.average_score, reviews.releases
                key = {'_id': artist_id}
                data = {'artist_name': artist, 'playcount': playcount,
                        'average_score': avg_score, 'releases': releases}
                COLLECTION.replace_one(key, data, True)
                print('{0} was loaded to MongoDB!'.format(data))
            except IndexError:
                print('{0} could not be loaded to the db'.format(a))


class ArtistIncr(object):

    def __init__(self, number_of_artists):
        self.artists = Artists(number_of_artists)

    def update_playcounts(self):
        for a in self.artists.artists_playcounts:
            artist_id, artist, playcount = a[0], a[1], a[2]
            key = {'_id': artist_id}
            COLLECTION.update_one(
                key, {'$set': {'playcount': playcount}}, upsert=True)
            print('The record for {0} was updated in MongoDB!'.format(artist))

    def update_ratings(self):
        for a in self.artists.artists_playcounts:
            try:
                releases = COLLECTION.find_one(
                    {'_id': a[0]}, {'_id': 0, 'releases': 1})['releases']
                new_releases = Reviews(a[0]).releases
                if set(releases) - set(new_releases) == set():
                    pass
                else:
                    reviews = Reviews(a[0])
                    artist_id, artist, playcount, avg_score, releases = a[
                        0], a[1], a[2], reviews.average_score, reviews.releases
                    key = {'_id': artist_id}
                    data = {'artist_name': artist, 'playcount': playcount,
                            'average_score': avg_score, 'releases': releases}
                    COLLECTION.replace_one(key, data, True)
                    print('{0} was updated to MongoDB!'.format(data))
            except (IndexError, KeyError):
                print('no releases!')
# psudocode
# for each artist
# 1. get the list of releases from Mongo
# 2. get the list of releases from Musikki
# 3. compare the two.

if __name__ == '__main__':
    from timeit import Timer
    number = 1
    a = Artists(number)
    t = Timer(lambda: a.artists_playcounts)
    t = t.timeit(number=number)
    print('the artist and playcount call takes {0} minutes'.format(
        str(t * 500 / 60)))
    r = Reviews('664c3e0e-42d8-48c1-b209-1efca19c0325')
    t = Timer(lambda: r.releases)
    t = t.timeit(number=number)
    print('the releases call takes {0} minutes'.format(str(t * 500 / 60)))
    t = Timer(lambda: r.average_score)
    t = t.timeit(number=number)
    print('the average score calculation takes {0} minutes'.format(
        str(t * 500 / 60)))
