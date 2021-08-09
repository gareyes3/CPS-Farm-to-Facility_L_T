# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 14:52:43 2021

@author: Gustavo Reyes
"""

import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from subprocess import call

app = dash.Dash(__name__)


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Farm to Facility Sampling Plans", style={'text-align': 'center'}),
    
    html.H2("Select a sampling Plan", style={'text-align': 'left'}),

    dcc.Dropdown(id="sel_Splan",
                 options=[
                      {"label": "No Sampling", "value": "Baseline"},
                     {"label": "Pre Harvest", "value": "PHS"},
                     {"label": "Harvest", "value": "HS"},
                     {"label": "Receiving", "value": "RS"},
                     {"label": "Final Producr", "value": "FPS"}],
                 multi=False,
                 value="Baseline",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    html.Button('Run Simulation', id='button'),
    html.Div(id='output-container-button',
    children='Hit the button to run simulation')

])


@app.callback(
dash.dependencies.Output('output-container-button', 'children'),
[dash.dependencies.Input('button', 'n_clicks')])
def run_script_onClick(n_clicks):
    # Don't run unless the button has been pressed...
    if not n_clicks:
        raise PreventUpdate

    script_path = 'C:\\Users\Gustavo Reyes\Documents\GitHubFiles\CPS-Farm-to-Facility\Model\ Play Script.py'
    # The output of a script is always done through a file dump.
    # Let's just say this call dumps some data into an `output_file`
    call(["python3", script_path])


    # Load your output file with "some code"
    output_content = some_loading_function('output file')
    return output_content



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server()