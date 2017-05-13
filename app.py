from flask import Flask, render_template
import bokeh.charts as bc
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from flask_pymongo import MongoClient
import pandas as pd


app = Flask(__name__)


@app.route("/albums")
def visualization():
    df = pd.read_csv('etl/csvs/album_frame.csv')
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    by_year = bc.Area(df.groupby('Year').size(),
                      title='Albums By Year', legend=None)

    by_decade = bc.Bar(df.groupby('Decade').size(),
                       title='Albums By Decade', legend=None)

    by_artist = bc.Line(df.groupby('Artist').size().sort_values(
        ascending=False).head(10), legend=None)

    by_genre = bc.Line(pd.read_csv('etl/csvs/genre.csv'), legend='top_right',
                       title='Albums by Genre')

    script, year_div = components(by_year)
    script2, decade_div = components(by_decade)
    artist_script, artist_div = components(by_artist)
    genre_script, genre_div = components(by_genre)

    html = render_template('year.html',
                           year_script=script,
                           decade_script=script2, decade_div=decade_div,
                           year_div=year_div,
                           artist_script=artist_script,
                           artist_div=artist_div,
                           genre_script=genre_script,
                           genre_div=genre_div,
                           js_resources=js_resources, css_resources=css_resources)

    return encode_utf8(html)


@app.route('/artists')
def artists_visualizatioons():
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    client = MongoClient('localhost', 27017)
    db = client['top_500']
    collection = db['artists']
    df = pd.DataFrame(list(collection.find(
        {'average_score': {'$ne': 'No Reviews'}}, {'artist_name': 1, 'playcount': 1, 'average_score': 1, '_id': 0}).sort('playcount', 1)))

    scatter = bc.Scatter(df, x='playcount', y='average_score', title="Album Rating vs Playcount",
                         xlabel="Last FM Playcount", ylabel="Average Album Rating")
    scatter_script, scatter_div = components(scatter)

    html = render_template('artists.html',
                           scatter_script=scatter_script,
                           scatter_div=scatter_div,
                           js_resources=js_resources,
                           css_resources=css_resources)

    return encode_utf8(html)


if __name__ == '__main__':
    app.run()
