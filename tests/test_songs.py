import unittest
from etl import songs


class ArtistTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ArtistTest.lfm = songs.Artists(500)

    def test_top_artist(self):
        self.assertEqual(
            {'664c3e0e-42d8-48c1-b209-1efca19c0325': ['The National', '780']}, ArtistTest.lfm.artists_playcounts[0])

    def test_151st_artist(self):
        self.assertEqual(
            {'fc7bbf00-fbaa-4736-986b-b3ac0266ca9b': ['alt-J', '68']}, ArtistTest.lfm.artists_playcounts[150])

    def test_last_artist(self):
        self.assertEqual(
            {'7f97f48f-d388-4e42-8068-d5b62a808aa3': ['Empires', '14']}, ArtistTest.lfm.artists_playcounts[-1])


class ReviewsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ReviewsTest.r = songs.Reviews('664c3e0e-42d8-48c1-b209-1efca19c0325')

    def test_mkid(self):
        self.assertEqual(100094349, ReviewsTest.r.mkid)

    def test_count_of_releases(self):
        self.assertEqual(6, len(ReviewsTest.r.releases))

    def test_most_recent_release(self):
        self.assertEqual([101252510, 'Trouble Will Find Me'],
                         ReviewsTest.r.releases[0])

    def test_earliest_release(self):
        self.assertEqual([100127863, 'The National'],
                         ReviewsTest.r.releases[-1])

    # def test_get_earliest_national_release(self):
    #     self.assertEqual([100127863, 'The National'],
    #                      ArtistTest.national_albums[-1])

    # def test_get_trouble_will_find_me_reviews_first(self):
    #     self.assertEqual({'value': 9.0, 'scale': 0.0},
    #                      ArtistTest.trouble_reviews[0])

    # def test_get_trouble_will_find_me_reviews_last(self):
    #     self.assertEqual({'value': 4.0, 'scale': 5.0},
    #                      ArtistTest.trouble_reviews[-1])

    # def test_get_trouble_will_find_me_reviews_number(self):
    #     self.assertEqual(7, len(ArtistTest.trouble_reviews))

    # def test_trouble_will_find_me_album_score(self):
    #     self.assertEqual(7.03, songs.album_score(ArtistTest.trouble_reviews))

    # def test_get_all_reviews_len(self):
    #     self.assertEqual(6, len(songs.get_all_reviews(
    #         ArtistTest.national_albums)))

    # def test_most_recent_review(self):
    #     self.assertEqual('Stuff', songs.get_all_reviews(
    #         ArtistTest.national_albums[0]))

    # def test_total_all_album_scores(self):
    #     self.assertEqual('in process', songs.get_all_album_scores(
    #         songs.get_all_reviews(ArtistTest.national_albums)))
