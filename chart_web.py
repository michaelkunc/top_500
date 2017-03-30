from flask import Flask, render_template

app = Flask(__name__)

import pandas as pd
import bokeh.charts as bc
from bokeh.resources import CDN
from bokeh.embed import components


@app.route("/")
def visualization():
    albums_by_year = pd.read_csv('csvs/albums_by_decade_year.csv',
                                 encoding="ISO-8859-1", header=None, names=['Decade', 'Year', 'Album Count'])

    by_year = bc.Bar(albums_by_year, 'Year', values='Album Count',
                     title='Albums By Year', legend=None, bar_width=.6)

    script, div = components(by_year)

 #    return """
    # <!doctype html>
    # <head>
    #  {bokeh_css}
    # </head>
    # <body>
    #  {div}
    #  {bokeh_js}
    #  {script}
    # </body>
    #  """.format(script=script, div=div, bokeh_css=CDN.render_css(),
 #             bokeh_js=CDN.render_js())
    return render_template('basic.html', script=script, div=div, bokeh_css=CDN.render_css(), bokeh_js=CDN.render_js())


if __name__ == '__main__':
    app.run()
