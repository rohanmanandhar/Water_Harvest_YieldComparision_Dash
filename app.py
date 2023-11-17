
# import libraries required for dash app
from dash import Dash, html, dcc
from jupyter_dash import JupyterDash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np

harvest=pd.read_excel("harvest.xlsx", sheet_name=2)

baseline=pd.read_excel("harvest.xlsx", sheet_name=0)

combined = harvest.merge(baseline, on="Land ID", suffixes=( "", "_B"))

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app=Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN, dbc_css])
server = app.server

load_figure_template("CERULEAN")


app.layout=dbc.Container([
    dcc.Tabs(className="dbc", children=[
        dbc.Tab(label="Yield Comparision", children=[
            html.H4(id="map2_title", style={"textAlign": "center"}),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Markdown("**Select a District:**"),
                        dcc.Checklist(
                            id='checklist_district',
                            options=[{'label': i, 'value': i} for i in sorted(harvest.District.unique())],
                            value=[],
                            className="dbc"
                        ),

                        dcc.Markdown("**Select Type of Crops:**"),
                        dcc.Checklist(
                            id='checklist_crops',
                            options=[{'label': i, 'value': i} for i in harvest.Crops.unique()],
                            value=[],
                            className="dbc"
                        ),

                    ])
                ], width=4),
                dbc.Col([
                    dcc.Graph(id='graph')
                ], width=8)
            ]),
            
            
        ])
    ])
])
        

@app.callback(
        Output('map2_title', 'children'),
        Output('graph', 'figure'),
        Input('checklist_district', 'value'),
        Input('checklist_crops', 'value')
)

def update_figure(district, crop): 
    
    if not district and not crop:
        title = "Total Baseline vs Current Yield in All Districts"
        df = combined

    elif district and not crop:
        title = f"Baseline vs Current Yield in Selected District/s"
        df = combined.query('District in @district')
    
    elif not district and crop:
        title = f"Baseline vs Current Yield in All Districts for Selected Crop/s"
        df = combined.query('Crops in @crop')
    
    else:
        title = f"Baseline vs Current Yield in Selected District/s for Selected Crop/s"
        df = combined.query('District in @district').query('Crops in @crop')

    
    # # Calculate the maximum count of respondents
    # max_count = df.groupby(["Gender"]).size().max()

    # # Calculate the step size based on the maximum count and the desired number of ticks
    # step_size = max(1, max_count // 6)

    # # Generate the tick values by starting from 0 and incrementing by the step size
    # tickvals = list(range(0, max_count + 2, step_size))

    fig=px.bar(
        df.groupby("District").agg({"Updated Yield": "sum", "Baseline Yield": "sum"}).reset_index().rename(columns={"Updated Yield": "Current Yield"}),
        x="District",
        y=["Baseline Yield", "Current Yield"],
        barmode="group",
        title="Baseline and Current Yield by District",
        labels={"value": "Yield (kg)", "variable": "Yield Type"},
        color_discrete_sequence=["orange", "cornflowerblue"]
    ).update_yaxes(
        tickformat='d'
    )
        
    return title, fig
    

app.run_server()
