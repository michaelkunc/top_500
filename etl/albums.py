import pandas as pd


class Albums(object):

    def __init__(self):
        self.df = pd.read_csv('etl/csvs/albumlist.csv', encoding="ISO-8859-1")

    def add_decade(self, row):
        if row['Year'] > 2010:
            return "2010's"
        if row['Year'] > 2000:
            return "2000's"
        if row['Year'] > 1990:
            return "1990's"
        if row['Year'] > 1980:
            return "1980's"
        if row['Year'] > 1970:
            return "1970's"
        if row["Year"] > 1960:
            return "1960's"
        else:
            return "1950's"

    def albums_by_artist(self, number_of_artists):
        return self.df.groupby('Artist').size().sort_values(ascending=False).head(number_of_artists)

    @property
    def albums_by_year(self):
        return self.df.groupby('Year').size()

    @property
    def albums_by_decade(self):
        self.df['Decade'] = self.df.apply(
            lambda row: self.add_decade(row), axis=1)
        return self.df.groupby('Decade').size()

    @property
    def albums_by_artist_top_ten(self):
        return self.df.groupby('Artist').size().sort_values(ascending=False).head(10)
