import unittest
from etl import albums


class Album_Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Album_Test.data = albums.Albums()

    def test_data_frame_shape(self):
        self.assertEqual((500, 7),
                         Album_Test.data.df.shape)

    def test_column_headers(self):
        self.assertEqual(['Number', 'Year', 'Album', 'Artist',
                          'Genre', 'Subgenre', 'Decade'], list(Album_Test.data.df.columns))

    def test_first_row(self):
        self.assertEqual([1, 1967, "Sgt. Pepper's Lonely Hearts Club Band", "The Beatles",
                          "Rock", "Rock & Roll, Psychedelic Rock", "1960's"], list(Album_Test.data.df.ix[0]))

    def test_min__max_years(self):
        self.assertEqual((1955, 2011),
                         tuple((int(Album_Test.data.df['Year'].min()), int(Album_Test.data.df['Year'].max()))))

    def test_albums_by_year_shape(self):
        self.assertEqual((56,), Album_Test.data.albums_by_year.shape)

    def test_albums_by_year_10th_row(self):
        self.assertEqual(14, Album_Test.data.albums_by_year.iloc[10])

    def test_albums_by_year_total(self):
        self.assertEqual(500, Album_Test.data.albums_by_year.sum())

    def test_albums_by_decade_shape(self):
        self.assertEqual((7,), Album_Test.data.albums_by_decade.shape)

    def test_albums_by_decade_5th_row(self):
        self.assertEqual(34, Album_Test.data.albums_by_decade.iloc[5])

    def test_albums_by_decade_total(self):
        self.assertEqual(500, Album_Test.data.albums_by_decade.sum())

    def test_albums_by_artist_top_ten_shape(self):
        self.assertEqual((10,), Album_Test.data.albums_by_artist_top_ten.shape)

    def test_albums_by_artist_top_ten_3rd_row(self):
        self.assertEqual(10, Album_Test.data.albums_by_artist_top_ten.iloc[2])

    def test_albums_by_artist_top_ten_total(self):
        self.assertEqual(70, Album_Test.data.albums_by_artist_top_ten.sum())
