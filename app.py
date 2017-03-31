from flask import Flask, render_template

app = Flask(__name__)

# import pandas as pd
import bokeh.charts as bc
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.util.string import encode_utf8
from etl import albums


@app.route("/")
def visualization():
    albums_by_year = albums.albums_by_year()
    # pd.read_csv('csvs/albums_by_decade_year.csv',
    # encoding = "ISO-8859-1", header = None, names = ['Decade', 'Year',
    # 'Album Count'])

    by_year = bc.Bar(albums_by_year, 'Year', values='Album Count',
                     title='Albums By Year', legend=None, bar_width=.6)

    by_decade = bc.Bar(albums_by_year, 'Decade', agg='sum', group='Decade', values='Album Count',
                       title='Albums By Decade', legend=None)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, year_div = components(by_year)
    script2, decade_div = components(by_decade)

    html = render_template('year.html', plot_script=script, decade_script=script2, plot_div=year_div, decade_div=decade_div,
                           js_resources=js_resources, css_resources=css_resources)

    return encode_utf8(html)

if __name__ == '__main__':
    app.run()
