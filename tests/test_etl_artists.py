import unittest
from etl import artists


class ArtistTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ArtistTest.lfm = artists.Artists(500)

    def test_top_artist(self):
        self.assertEqual(
            ['664c3e0e-42d8-48c1-b209-1efca19c0325', 'The National', '780'], ArtistTest.lfm.artists_playcounts[0])

    def test_151st_artist(self):
        self.assertEqual(
            ['fc7bbf00-fbaa-4736-986b-b3ac0266ca9b', 'alt-J', '68'], ArtistTest.lfm.artists_playcounts[150])

    def test_last_artist(self):
        self.assertEqual(
            ['7f97f48f-d388-4e42-8068-d5b62a808aa3', 'Empires', '14'], ArtistTest.lfm.artists_playcounts[-1])


class ReviewsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ReviewsTest.r = artists.Reviews('664c3e0e-42d8-48c1-b209-1efca19c0325')

    def test_mkid(self):
        self.assertEqual(100094349, ReviewsTest.r.mkid)

    def test_count_of_releases(self):
        self.assertEqual(6, len(ReviewsTest.r.releases))

    def test_most_recent_release(self):
        self.assertEqual(101252510,
                         ReviewsTest.r.releases[0])

    def test_earliest_release(self):
        self.assertEqual(100127863,
                         ReviewsTest.r.releases[-1])

    def test_reviews(self):
        self.assertEqual(18, len(ReviewsTest.r.reviews))

    def test_most_recent_trouble_will_find_me_review(self):
        self.assertEqual({'value': 9.0, 'scale': 0.0},
                         ReviewsTest.r.reviews[-18])

    def test_most_recent_high_violet_review(self):
        self.assertEqual({"value": 3.5, "scale": 5},
                         ReviewsTest.r.reviews[-11])

    def test_earliest_boxer_review(self):
        self.assertEqual({'value': 4, "scale": 5}, ReviewsTest.r.reviews[-4])

    def test_average_score(self):
        self.assertEqual(7.49, ReviewsTest.r.average_score)


class ArtistIncrTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ArtistIncrTest.a = artists.ArtistIncr(10, 'top_500', 'artists')

    def test_len_artists(self):
        self.assertEqual(10, len(ArtistIncrTest.a.artists.artists_playcounts))

    def test_len_first_result(self):
        self.assertEqual(
            3, len(ArtistIncrTest.a.artists.artists_playcounts[0]))
