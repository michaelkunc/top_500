import pandas as pd
df = pd.read_csv('csvs/albumlist.csv', encoding="ISO-8859-1")


# add needed attributes to df
def add_decade(row):
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
df['Decade'] = df.apply(lambda row: add_decade(row), axis=1)

# albums_by_decade_year = df.groupby(['Decade', 'Year']).size()
# albums_by_decade_year.columns = ['Decade', 'Year', 'Album Count']
# albums_by_decade_year.to_csv('csvs/albums_by_decade.csv')


def group_and_export(Attribute):
    if isinstance(Attribute, list):
        return df.groupby(Attribute).size().to_csv('csvs/albums_by_{}.csv'.format('_'.join(Attribute).lower()))
    else:
        return df.groupby(Attribute).size().to_csv('csvs/albums_by_{}.csv'.format(Attribute.lower()))


# various group-by and exports
group_and_export(['Decade', 'Year'])

group_and_export('Artist')

group_and_export('Genre')
