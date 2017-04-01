import unittest
from etl import albums


class Album_Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Album_Test.data = albums.Albums()

    def test_data_frame_shape(self):
        self.assertEqual((500, 6),
                         Album_Test.data.df.shape)

    def test_column_headers(self):
        self.assertEqual(['Number', 'Year', 'Album', 'Artist',
                          'Genre', 'Subgenre'], list(Album_Test.data.df.columns))

    def test_first_row(self):
        self.assertEqual([1, 1967, "Sgt. Pepper's Lonely Hearts Club Band", "The Beatles",
                          "Rock", "Rock & Roll, Psychedelic Rock"], list(Album_Test.data.df.ix[0]))

    def test_max_min_years(self):
        self.assertEqual((1955, 2011), list(
            Album_Test.data.df['Year'].min()))
