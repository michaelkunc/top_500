from flask import Flask, render_template

import bokeh.charts as bc
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from etl import albums

app = Flask(__name__)


@app.route("/")
def visualization():
    album_df = albums.Albums()
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    by_year = bc.Area(album_df.group_by_attribute('Year'),
                      title='Albums By Year', legend=None)

    by_decade = bc.Bar(album_df.group_by_attribute('Decade'),
                       title='Albums By Decade', legend=None)

    by_artist = bc.Line(album_df.albums_by_artist(), legend=None)

    by_genre = bc.Line(album_df.scatter_plot_sample_data(),
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

if __name__ == '__main__':
    app.run()
