import pandas as pd


class Albums(object):

    def __init__(self):
        self.df = pd.read_csv('etl/csvs/albumlist.csv', encoding="ISO-8859-1")

    def add_decade(self, row):
        if row['Year'] > 2010:
            return "10's"
        if row['Year'] > 2000:
            return "00's"
        if row['Year'] > 1990:
            return "90's"
        if row['Year'] > 1980:
            return "80's"
        if row['Year'] > 1970:
            return "70's"
        if row["Year"] > 1960:
            return "60's"
        else:
            return "50's"

    @property
    def albums_by_year(self):
        return self.df.groupby('Year').size()

    @property
    def albums_by_decade(self):
        self.df['Decade'] = self.df.apply(
            lambda row: self.add_decade(row), axis=1)
        return self.df.groupby('Decade').size()

# album = Album()
# print(album.albums_by_year)
