import pandas as pd


def albums_by_year():
    return pd.read_csv('etl/csvs/albums_by_decade_year.csv',
                       encoding="ISO-8859-1", header=None, names=['Decade', 'Year', 'Album Count'])
