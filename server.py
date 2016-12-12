from flask import Flask
from flask import request


import plotly.graph_objs as go
import plotly.offline as offline
from plotly import tools
import numpy as np

import pandas as pd


offline.init_notebook_mode() 

app = Flask(__name__, static_url_path='/static')
   
    
@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/test')
def test():

    x = np.random.randn(2000)
    y = np.random.randn(2000)

    data = [
        go.Histogram2dContour(x=x, y=y, contours=go.Contours(coloring='heatmap')),
        go.Scatter(x=x, y=y, mode='markers', marker=go.Marker(color='white', size=3, opacity=0.3))
    ]

    layout = go.Layout(
        title="Test",
        autosize=False,
        width=500,
        height=500,
        xaxis=dict(title="Testx"),
        yaxis=dict(title="Testy")
    )
    fig = go.Figure(data=data, layout=layout)
    div = offline.plot(fig,  output_type="div")
    return div;