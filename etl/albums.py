import pandas as pd
from collections import Counter


class Albums(object):

    def __init__(self):
        self.df = pd.read_csv('etl/csvs/albumlist.csv', encoding="ISO-8859-1")
        self.df['Decade'] = self.df.apply(
            lambda row: self._add_decade(row), axis=1)
        self.df = self._normalize_genre()

    def albums_by_artist(self, number_of_artists=10):
        return self.df.groupby('Artist').size().sort_values(ascending=False).head(number_of_artists)

    def group_by_attribute(self, attribute):
        return self.df.groupby(attribute).size()

    def _add_decade(self, row):
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

# in development for powering the scatter plot
    def scatter_plot_sample_data(self):
        return pd.DataFrame.from_dict({'1955': Counter(['Pop', 'Rock', 'Rock', 'Rock', 'Pop', 'Pop', 'Pop', 'Blues']),
                                       '1956': Counter(['Rock', 'Rock', 'Rock', 'Pop', 'Pop', 'Rock']),
                                       '1957': Counter(['Funk', 'Soul', 'Rock', 'Rock', 'Blues', 'Rock', 'Pop', 'Jazz'])},
                                      orient='index').fillna(0)

    def _normalize_genre(self):
        self.df['normalized_genre'] = self.df['Genre'].str.replace(' & ', '')
        self.df['normalized_genre'] = self.df[
            'normalized_genre'].str.replace(' / ', ',')
        self.df['normalized_genre'] = self.df[
            'normalized_genre'].str.replace(', ', ',')
        return self.df
