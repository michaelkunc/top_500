import numpy as np
import pandas as pd
import bokeh.charts as bc

from bokeh.plotting import output_file, show

df = pd.DataFrame({
    'x': 2 * np.pi * i / 100,
    'sin': np.sin(2 * np.pi * i / 100),
    'cos': np.cos(2 * np.pi * i / 100),
} for i in range(0, 101))

output_file = ('myplot.html')

plot = bc.Line(title='getting started', data=df, x='x', ylabel='y')
show(plot)
