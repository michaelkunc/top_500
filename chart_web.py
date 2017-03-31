from flask import Flask, render_template

app = Flask(__name__)

import pandas as pd
import bokeh.charts as bc
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.util.string import encode_utf8


@app.route("/")
def visualization():
    albums_by_year = pd.read_csv('csvs/albums_by_decade_year.csv',
                                 encoding="ISO-8859-1", header=None, names=['Decade', 'Year', 'Album Count'])

    by_year = bc.Bar(albums_by_year, 'Year', values='Album Count',
                     title='Albums By Year', legend=None, bar_width=.6)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(by_year)

    html = render_template('basic.html', plot_script=script, plot_div=div,
                           js_resources=js_resources, css_resources=css_resources)

    return encode_utf8(html)

if __name__ == '__main__':
    app.run()
