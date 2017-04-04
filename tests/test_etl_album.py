import unittest
from etl import albums


class Album_Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Album_Test.data = albums.Albums()

    def test_data_frame_shape(self):
        self.assertEqual((500, 8),
                         Album_Test.data.df.shape)

    def test_column_headers(self):
        self.assertEqual(['Number', 'Year', 'Album', 'Artist',
                          'Genre', 'Subgenre', 'Decade', 'normalized_genre'], list(Album_Test.data.df.columns))

    def test_first_row(self):
        self.assertEqual([1, 1967, "Sgt. Pepper's Lonely Hearts Club Band", "The Beatles",
                          "Rock", "Rock & Roll, Psychedelic Rock", "1960's", 'Rock'], list(Album_Test.data.df.ix[0]))

    def test_min__max_years(self):
        self.assertEqual((1955, 2011), tuple(
            (int(Album_Test.data.df['Year'].min()), int(Album_Test.data.df['Year'].max()))))

    def test_albums_by_year_shape(self):
        self.assertEqual(
            (56,), Album_Test.data.group_by_attribute('Year').shape)

    def test_albums_by_year_10th_row(self):
        self.assertEqual(
            14, Album_Test.data.group_by_attribute('Year').iloc[10])

    def test_albums_by_year_total(self):
        self.assertEqual(500, Album_Test.data.group_by_attribute('Year').sum())

    def test_albums_by_decade_shape(self):
        self.assertEqual(
            (7,), Album_Test.data.group_by_attribute('Decade').shape)

    def test_albums_by_decade_5th_row(self):
        self.assertEqual(
            34, Album_Test.data.group_by_attribute('Decade').iloc[5])

    def test_albums_by_decade_total(self):
        self.assertEqual(
            500, Album_Test.data.group_by_attribute('Decade').sum())

    def test_albums_by_artist_top_ten_shape(self):
        self.assertEqual((10,), Album_Test.data.albums_by_artist(10).shape)

    def test_albums_by_artist_top_ten_3rd_row(self):
        self.assertEqual(10, Album_Test.data.albums_by_artist(10).iloc[2])

    def test_albums_by_artist_top_ten_total(self):
        self.assertEqual(70, Album_Test.data.albums_by_artist(10).sum())

    def test_normalize_genre_ampersand(self):
        self.assertEqual('Folk,World,Country', Album_Test.data.df[
                         'normalized_genre'].iloc[476])

    def test_normalize_genre_slash(self):
        self.assertEqual('Hip Hop,Funk,Soul', Album_Test.data.df[
                         'normalized_genre'].iloc[480])

    def test_normalize_genre_extra_space(self):
        self.assertEqual('Rock,Blues', Album_Test.data.df[
                         'normalized_genre'].iloc[8])
