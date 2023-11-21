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

df=pd.read_csv("tracker.csv")
df.columns = df.columns.str.strip()

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app=Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])
server = app.server

load_figure_template("SLATE")

app.layout = dbc.Container([
    dbc.Tabs(class_name="dbc", children=[
            dbc.Tab(label="Location Wise", children=[
                html.Br(),
                dbc.Row([
                    dbc.Col([
                            dbc.Card([
                            dcc.Markdown("**Select Implementation Status**"),
                            dcc.Dropdown(
                                id="Implementation_Status",
                                options=[{"label": i, "value": i} for i in ["Completed", "Underway", "With Procurement", "In Development"] if i in df["Overall Status"].unique()],
                                value = [],
                                className="dbc"
                            ),
                            dcc.Markdown("**Select Sector**"),
                            dcc.Dropdown(
                                id="sector_picker",
                                options=[{"label": i, "value": i} for i in df["Sector"].unique()],
                                value=[],
                                multi=True,
                                className="dbc"
                            )
                        ]),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            dbc.Card([
                                dcc.Markdown("**Summary of plotted data**"),
                                dbc.Card(id="activitySummary"),
                                dbc.Card(id="amountSummary"),
                            ])
                            
                    ], width=4),
                    dbc.Col([
                        html.Br(),
                        html.H4(id="map1-title", style={"text-align": "center"}),
                        html.Br(),
                        dcc.Graph(id="graph1", style={'height': '37.5vh'}),
                        html.Br(),
                        html.H4(id="map2-title", style={"text-align": "center"}),
                        html.Br(),
                        dcc.Graph(id="graph2", style={'height': '37.5vh'})
                    ], width=8)
                ])
            ]), # End of Location Wise Tab - 1

            dbc.Tab(label="Sector Wise", children=[
                html.Br(),
                dbc.Row([
                    dbc.Col([
                            dbc.Card([
                            dcc.Markdown("**Select Implementation Status**"),
                            dcc.Dropdown(
                                id="Implementation_Status2",
                                options=[{"label": i, "value": i} for i in ["Completed", "Underway", "With Procurement", "In Development"] if i in df["Overall Status"].unique()],
                                value = [],
                                className="dbc"
                            ),
                            dcc.Markdown("**Select Location**"),
                            dcc.Dropdown(
                                id="location_picker",
                                options=[{"label": i, "value": i} for i in sorted(df["Location"].unique())],
                                value=[],
                                multi=True,
                                className="dbc"
                            )
                        ]),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            dbc.Card([
                                dcc.Markdown("**Summary of plotted data**"),
                                dbc.Card(id="activitySummary2"),
                                dbc.Card(id="amountSummary2"),
                            ])
                            
                    ], width=4),
                    dbc.Col([
                        html.Br(),
                        html.H4(id="map3-title", style={"text-align": "center"}),
                        html.Br(),
                        dcc.Graph(id="graph3", style={'height': '37.5vh'}),
                        html.Br(),
                        html.H4(id="map4-title", style={"text-align": "center"}),
                        html.Br(),
                        dcc.Graph(id="graph4", style={'height': '37.5vh'})
                    ], width=8)
                ])
            ]), # End of Sector Wise Tab - 2
    ])
])

@app.callback(
    Output("map1-title", "children"),
    Output("graph1", "figure"),
    Input("Implementation_Status", "value"),
    Input("sector_picker", "value")
)

def update_map1(status, sector):
    
    
    if not status and not sector:
        title = "Number of Activities"
        sfl = df
        sfl_sum = sfl.groupby("Location").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Location").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Location")
    
    elif status and not sector:
        title = f"Number of '{status}' Activities"
        sfl = df.query("`Overall Status` in @status")
        sfl_sum = sfl.groupby("Location").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Location").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Location")

    elif not status and sector:
        title = f"Number of Activities"
        sfl = df.query("`Sector` in @sector")
        sfl_sum = sfl.groupby("Location").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Location").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Location")

    else:
        title = f"Number of '{status}' Activities"
        sfl = df.query("`Overall Status` in @status").query("`Sector` in @sector")
        sfl_sum = sfl.groupby("Location").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Location").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Location")

        
    
    fig = px.bar(
    sfl_merged.sort_values("Number of Activities", ascending=False),
    x="Location",
    y="Number of Activities",
    text="Number of Activities",
    hover_data={"Amount": ":.2f"},
    hover_name="Location", # Use "Location" as hover name
    ).update_traces(
    textposition='outside',
    hovertemplate="<b style='font-size: 15px;'>%{hovertext}</b><br><br>Number of Activities: %{y}<br>Amount: US$ %{customdata[0]:.2f} M", # Customise hover template
    marker_color='lightblue'  # Set bar color
    ).update_layout(
    showlegend=False,
    ).update_yaxes(  # Add some padding to the y-axis
    range=[0, 1.1 * sfl_merged["Number of Activities"].max()],
    )

    return title, fig


@app.callback(
    Output("activitySummary", "children"),
    Output("amountSummary", "children"),
    Input("Implementation_Status", "value"),
    Input("sector_picker", "value")
)

def update_summary1(status, sector):
    if not status and not sector:
        sfl = df
        sfl_sum = sfl.groupby("Location").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Location").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Location")
    
    elif status and not sector:
        sfl = df.query("`Overall Status` in @status")
        sfl_sum = sfl.groupby("Location").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Location").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Location")

    elif not status and sector:
        sfl = df.query("`Sector` in @sector")
        sfl_sum = sfl.groupby("Location").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Location").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Location")

    else:
        sfl = df.query("`Overall Status` in @status").query("`Sector` in @sector")
        sfl_sum = sfl.groupby("Location").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Location").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Location")

    activity = f"Number of Activities: {sfl_merged['Number of Activities'].sum()}" 
    amount = f"Amount in US$ (million): {sfl_merged['Amount'].sum():.2f}"

    return activity, amount

@app.callback(
    Output("map2-title", "children"),
    Output("graph2", "figure"),
    Input("Implementation_Status", "value"),
    Input("sector_picker", "value")
)


def update_map2(status, sector):
    
    
    if not status and not sector:
        title = "Fund Allocation"
        sfl = df
        sfl_sum = sfl.groupby("Location").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Location").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Location").sort_values("Number of Activities", ascending=False)
    
    elif status and not sector:
        title = f"Fund Allocation for '{status}' Activities"
        sfl = df.query("`Overall Status` in @status")
        sfl_sum = sfl.groupby("Location").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Location").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Location").sort_values("Number of Activities", ascending=False)

    elif not status and sector:
        title = f"Fund Allocation"
        sfl = df.query("`Sector` in @sector")
        sfl_sum = sfl.groupby("Location").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Location").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Location").sort_values("Number of Activities", ascending=False)

    else:
        title = f"Fund Allocation for '{status}' Activities"
        sfl = df.query("`Overall Status` in @status").query("`Sector` in @sector")
        sfl_sum = sfl.groupby("Location").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Location").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Location").sort_values("Number of Activities", ascending=False)

        
    
    fig = px.bar(
    sfl_merged,
    x="Location",
    y="Amount",
    text=sfl_merged["Amount"].apply(lambda x: f'{x:.2f}'),  # Format text as two decimal points
    hover_data={"Number of Activities"},
    hover_name="Location", # Use "Location" as hover name
    ).update_traces(
    textposition='outside',
    hovertemplate="<b style='font-size: 15px;'>%{hovertext}</b><br><br>Amount: %{y:.2f}<br>Number of Activities: %{customdata[0]}", # Customise hover template
    marker_color='olive'  # Set bar color
    ).update_layout(
    showlegend=False,
    ).update_yaxes(  # Add some padding to the y-axis
    range=[0, 1.1 * sfl_merged["Amount"].max()],
    title_text='Amount in Million US$'  # Set y-axis label
    )

    return title, fig # End of Location Wise Tab - 1


@app.callback(
    Output("map3-title", "children"),
    Output("graph3", "figure"),
    Input("Implementation_Status2", "value"),
    Input("location_picker", "value")
)

def update_map3(status, location):
    
    
    if not status and not location:
        title = "Number of Activities"
        sfl = df
        sfl_sum = sfl.groupby("Sector").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Sector").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Sector")
        
    
    elif status and not location:
        title = f"Number of '{status}' Activities"
        sfl = df.query("`Overall Status` in @status")
        sfl_sum = sfl.groupby("Sector").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Sector").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Sector")

    elif not status and location:
        title = f"Number of Activities"
        sfl = df.query("`Location` in @location")
        sfl_sum = sfl.groupby("Sector").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Sector").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Sector")

    else:
        title = f"Number of '{status}' Activities"
        sfl = df.query("`Overall Status` in @status").query("`Location` in @location")
        sfl_sum = sfl.groupby("Sector").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Sector").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Sector")

        
    
    fig = px.bar(
    sfl_merged.sort_values("Number of Activities", ascending=False),
    x="Sector",
    y="Number of Activities",
    text="Number of Activities",
    hover_data={"Amount": ":.2f"},
    hover_name="Sector", # Use "Location" as hover name
    ).update_traces(
    textposition='outside',
    hovertemplate="<b style='font-size: 15px;'>%{hovertext}</b><br><br>Number of Activities: %{y}<br>Amount: US$ %{customdata[0]:.2f} M", # Customise hover template
    marker_color='lightblue'  # Set bar color
    ).update_layout(
    showlegend=False,
    ).update_yaxes(  # Add some padding to the y-axis
    range=[0, 1.2 * sfl_merged["Number of Activities"].max()],
    )

    return title, fig


@app.callback(
    Output("activitySummary2", "children"),
    Output("amountSummary2", "children"),
    Input("Implementation_Status2", "value"),
    Input("location_picker", "value")
)

def update_summary1(status, location):
    if not status and not location:
        sfl = df
        sfl_sum = sfl.groupby("Sector").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Sector").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Sector")
    
    elif status and not location:
        sfl = df.query("`Overall Status` in @status")
        sfl_sum = sfl.groupby("Sector").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Sector").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Sector")

    elif not status and location:
        sfl = df.query("`Location` in @location")
        sfl_sum = sfl.groupby("Sector").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Sector").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Sector")

    else:
        sfl = df.query("`Overall Status` in @status").query("`Location` in @location")
        sfl_sum = sfl.groupby("Sector").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Sector").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Sector")

    activity = f"Number of Activities: {sfl_merged['Number of Activities'].sum()}" 
    amount = f"Amount in US$ (million): {sfl_merged['Amount'].sum():.2f}"

    return activity, amount

@app.callback(
    Output("map4-title", "children"),
    Output("graph4", "figure"),
    Input("Implementation_Status2", "value"),
    Input("location_picker", "value")
)


def update_map4(status, location):
    
    
    if not status and not location:
        title = "Fund Allocation"
        sfl = df
        sfl_sum = sfl.groupby("Sector").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Sector").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Sector").sort_values("Number of Activities", ascending=False)
    
    elif status and not location:
        title = f"Fund Allocation for '{status}' Activities"
        sfl = df.query("`Overall Status` in @status")
        sfl_sum = sfl.groupby("Sector").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Sector").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Sector").sort_values("Number of Activities", ascending=False)

    elif not status and location:
        title = f"Fund Allocation"
        sfl = df.query("`Location` in @location")
        sfl_sum = sfl.groupby("Sector").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Sector").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Sector").sort_values("Number of Activities", ascending=False)

    else:
        title = f"Fund Allocation for '{status}' Activities"
        sfl = df.query("`Overall Status` in @status").query("`Location` in @location")
        sfl_sum = sfl.groupby("Sector").agg({"Amount": "sum"}).reset_index()
        sfl_sum["Amount"] = sfl_sum["Amount"] / 1e6  # Convert "Amount" to millions
        sfl_count = sfl.groupby("Sector").size().reset_index(name="Number of Activities")
        sfl_merged = pd.merge(sfl_count, sfl_sum, on="Sector").sort_values("Number of Activities", ascending=False)

        
    
    fig = px.bar(
    sfl_merged,
    x="Sector",
    y="Amount",
    text=sfl_merged["Amount"].apply(lambda x: f'{x:.2f}'),  # Format text as two decimal points
    hover_data={"Number of Activities"},
    hover_name="Sector", # Use "Location" as hover name
    ).update_traces(
    textposition='outside',
    hovertemplate="<b style='font-size: 15px;'>%{hovertext}</b><br><br>Amount: %{y:.2f}<br>Number of Activities: %{customdata[0]}", # Customise hover template
    marker_color='olive'  # Set bar color
    ).update_layout(
    showlegend=False,
    ).update_yaxes(  # Add some padding to the y-axis
    range=[0, 1.2 * sfl_merged["Amount"].max()],
    title_text='Amount in Million US$'  # Set y-axis label
    )

    return title, fig # End of Sector Wise Tab - 1
