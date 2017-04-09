import unittest
from etl import songs


class SongTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SongTest.national_albums = songs.get_releases(100094349)
        SongTest.trouble_reviews = songs.get_reviews(101252510)

    def test_top_artist(self):
        self.assertEqual(
            {'664c3e0e-42d8-48c1-b209-1efca19c0325': ['The National', '780']}, songs.last_fm_top_artists()[0])

    # def test_150th_artist(self):
    #     self.assertEqual({'alt-J': '68'}, songs.last_fm_top_artists()[150])

    def test_musikki_mkid(self):
        self.assertEqual(100094349, songs.musikki_mkid(
            '664c3e0e-42d8-48c1-b209-1efca19c0325'))

    def test_get_most_recent_national_release(self):
        self.assertEqual([101252510, 'Trouble Will Find Me'],
                         SongTest.national_albums[0])

    def test_get_earliest_national_release(self):
        self.assertEqual([100127863, 'The National'],
                         SongTest.national_albums[-1])

    def test_count_of_national_releases(self):
        self.assertEqual(6, len(SongTest.national_albums))

    def test_get_trouble_will_find_me_reviews_first(self):
        self.assertEqual({'value': 9.0, 'scale': 0.0},
                         SongTest.trouble_reviews[0])

    def test_get_trouble_will_find_me_reviews_last(self):
        self.assertEqual({'value': 4.0, 'scale': 5.0},
                         SongTest.trouble_reviews[-1])

    def test_get_trouble_will_find_me_reviews_number(self):
        self.assertEqual(7, len(SongTest.trouble_reviews))

    def test_album_score(self):
        self.assertEqual(7.03, songs.album_score(SongTest.trouble_reviews))

    # def test_get_all_reviews_len(self):
    #     self.assertEqual(6, len(songs.get_all_reviews(
    #         SongTest.national_albums)))

    # def test_total_all_album_scores(self):
    #     self.assertEqual('in process', songs.get_all_album_scores(
    #         songs.get_all_reviews(SongTest.national_albums)))
