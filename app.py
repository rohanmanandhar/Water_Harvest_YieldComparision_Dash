# import libraries required for dash app
from dash import Dash, html, dcc
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
        dbc.Tab(label="Satisfaction & Impact Perception", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Markdown("**Select a District:**"),
                        dcc.Checklist(
                            id='checklist_district_satisfaction',
                            options=[{'label': i, 'value': i} for i in sorted(harvest.District.unique())],
                            value=[],
                            className="dbc"
                        ),

                        dcc.Markdown("**Select Age Range:**"),
                        dcc.RangeSlider(
                            id='slider_satisfaction',
                            min = harvest.Age.min(),
                            max = harvest.Age.max(),
                            value = [],
                            step=5,
                            # marks={harvest.Age.min(): str(harvest.Age.min()),
                            #        20: "20",
                            #        25: "25",
                            #         30: "30",
                            #         35: "35",
                            #         40: "40",
                            #         45: "45",
                            #         50: "50",
                            #        harvest.Age.max(): str(harvest.Age.max())},
                            className="dbc"
                        ),

                    ])
                ], width=4),
                dbc.Col([
                    html.Br(),
                    html.H4(id="map4_title", style={"textAlign": "center"}),
                    html.Br(),
                    dcc.Graph(id='graph4', style={'height': '37.5vh'}), # To control the height of the graph
                    html.H4(id="map5_title", style={"textAlign": "center"}),
                    html.Br(),
                    dcc.Graph(id='graph5', style={'height': '37.5vh'}), # To control the height of the graph
                ], width=8)
            ]),
            
            
        ])
    ])
])
        

@app.callback(
        Output('map4_title', 'children'),
        Output('graph4', 'figure'),
        Input('checklist_district_satisfaction', 'value'),
        Input('slider_satisfaction', 'value')
)


def update_figure4(district, age): 

    # Replace 'F' and 'M' with 'Female' and 'Male'
    harvest['Gender'] = harvest['Gender'].replace({'F': 'Female', 'M': 'Male'})
    
    if not district and not age:
        title = "Overall Community Satisfaction Level by Gender"
        df = harvest

    elif district and not age:
        title = f"Community Satisfaction Level in {district}"
        df = harvest.query('District in @district')
    
    elif not district and age:
        title = f"Community Satisfaction Level of Respondents between age {age[0]} and {age[1]}"
        df = harvest[harvest['Age'].between(age[0], age[1])]
    
    else:
        title = f"Community Satisfaction Level of Respondents in {district} between age {age[0]} and {age[1]}"
        df = harvest.query('District in @district').query('Age >= @age[0] and Age <= @age[1]')
   

    fig=px.bar(
        df.groupby(["District", "Gender"]).agg({"Satisfaction": "mean"}).reset_index(),
        x="District",
        y=["Satisfaction"],
        color="Gender",
        barmode="group",
        labels={"value": "Satisfaction Level", "variable": "Gender"},
        color_discrete_map={"Female": "hotpink", "Male": "cornflowerblue"},
        # hover_data={"Satisfaction": ":.2f"}  # Add this line
    ).update_yaxes(
        tickformat='.2f',
        range=[0, 5] # to make y ticks to 5
    ).update_layout(
    annotations=[
        dict(
            x=0,
            y=1.15,
            showarrow=False,
            text="<i>Measured on a Scale of 1 to 5<i>",
            xref="paper",
            yref="paper",
            font=dict(
                color="brown"  # Change the color to your desired color
            )
        )
    ]
)
        
    return title, fig


@app.callback(
        Output('map5_title', 'children'),
        Output('graph5', 'figure'),
        Input('checklist_district_satisfaction', 'value'),
        Input('slider_satisfaction', 'value')
)


def update_figure5(district, age): 

    # Replace 'F' and 'M' with 'Female' and 'Male'
    harvest['Gender'] = harvest['Gender'].replace({'F': 'Female', 'M': 'Male'})
    
    if not district and not age:
        title = "Overall Impact Perception Level by Gender"
        df = harvest

    elif district and not age:
        title = f"Impact Perception Level in {district}"
        df = harvest.query('District in @district')
    
    elif not district and age:
        title = f"Impact Perception Level of Respondents between age {age[0]} and {age[1]}"
        df = harvest[harvest['Age'].between(age[0], age[1])]
    
    else:
        title = f"Impact Perception Level of Respondents in {district} between age {age[0]} and {age[1]}"
        df = harvest.query('District in @district').query('Age >= @age[0] and Age <= @age[1]')
   

    fig=px.bar(
        df.groupby(["District", "Gender"]).agg({"Perception": "mean"}).reset_index(),
        x="District",
        y=["Perception"],
        color="Gender",
        barmode="group",
        labels={"value": "Impact Perception Level", "variable": "Gender"},
        color_discrete_map={"Female": "hotpink", "Male": "cornflowerblue"},
        # hover_data={"Satisfaction": ":.2f"}  # Add this line
    ).update_yaxes(
        tickformat='.2f',
        range=[0, 5] # to make y ticks to 5
    ).update_layout(
    annotations=[
        dict(
            x=0,
            y=1.15,
            showarrow=False,
            text="<i>Measured on a Scale of 1 to 5<i>",
            xref="paper",
            yref="paper",
            font=dict(
                color="brown"  # Change the color to your desired color
            )
        )
    ]
)
        
    return title, fig
    

# app.run_server()
