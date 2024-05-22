# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 11:14:52 2023
@author: GOPESH KHANNA
"""

#%% Set up environment

# Set up environment
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pylab import rcParams
import seaborn as sns
import matplotlib.pyplot as plt
import dash
from dash import Input, Output
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
import geopandas as gpd


# Set plot parameters
rcParams['figure.figsize'] = 12, 8
rcParams['font.family'] = 'StixGeneral'
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False
rcParams['figure.dpi'] = 350
rcParams['lines.linewidth'] = 2

#%% Dashboard

un_logo_path = r'assets/UN_logo.jpeg'

# Select the bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

# Callback to update the year dropdown options based on the selected dataset
@app.callback(
    Output('country-dropdown', 'options'),
    [Input('datasets-dropdown', 'value')]
)
def update_country_dropdown(selected_dataset):
    filtered_df = pd.read_csv("cleaned_datasets/"+selected_dataset+".csv")
    countries = filtered_df['Country'].unique()
    options = [{'label': country, 'value': country} for country in countries]
    return options


# Create a drop down for datasets
datasets = ["GDP", "Unemployment", "Population", "Education"]
datasets_dropdown = dbc.Select(
    id='datasets-dropdown',
    options=[{'label': dataset, 'value': dataset} for dataset in datasets],
    value='GDP',  # Default selected country
    style={'width': '100%', 'display': 'inline-block', 'margin-right': '0px', 'background-color': '#333', 'color': '#fff'}  
)

#Reference for sidebar: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
# Sidebar style
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#333",
    "color": "#fff",
    "border-radius": "10px",  
    "z-index": 1,
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "color": "#fff",
    "background-color":"#000"
}

# Homepage Layout - ChatGPT
home_layout = html.Div(
    [
        html.H1("Welcome to the UN Dashboard", style={'text-align': 'center', 'margin-bottom': '20px'}),
        
        html.Div(
            [
                html.H2("Introduction", style={'margin-bottom': '10px'}),
                html.P(
                    "Explore and visualize United Nations data with our interactive dashboard. "
                    "Select different datasets, countries, and years to discover insights about "
                    "GDP, Unemployment, Population, and Education."
                ),
            ],
            style={'background-color': '#222', 'padding': '20px', 'border-radius': '10px', 'margin-bottom': '20px', "width":'100%'}
        ),
        
        html.Div(
            [
                html.H2("Dashboard Overview", style={'margin-bottom': '10px'}),
                html.P(
                    "The dashboard provides visualizations for different datasets. "
                    "Navigate through the pages using the sidebar menu:"
                ),
                html.Ul(
                    [
                        html.Li("Choropleth: Explore geographical data using interactive maps."),
                        html.Li("Bar Chart: Visualize dataset trends for a specific country."),
                        html.Li("Line Chart: Compare dataset trends across multiple countries."),
                    ]
                ),
            ],
            style={'background-color': '#333', 'padding': '20px', 'border-radius': '10px', 'margin-bottom': '20px',"width":'100%'}
        ),
        
        html.Div(
            [
                html.H2("Get Started", style={'margin-bottom': '10px'}),
                html.P(
                    "Click on the sidebar menu to start exploring the data. Choose a dataset, "
                    "select countries and years, and discover valuable insights. Enjoy your exploration!"
                ),
            ],
            style={'background-color': '#222', 'padding': '20px', 'border-radius': '10px', "width":'100%'}
        ),
    ],
)

sidebar = html.Div(
    [
         html.Div([
        html.Img(src=un_logo_path, alt='UN Logo', style={'width': '75px', 'height': '75px', 'margin-right': '10px'}),
        dcc.Markdown(
            '''
            **United**
            ** Nations**
            ''',
            style={'font-size': '24px', 'margin': '0', 'padding': '0'}
        )
    ], style={'display': 'flex', 'align-items': 'center'}),

        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Choropleth", href="/page-1", active="exact",style={"background-color": "burgundy"}),
                dbc.NavLink("Bar Chart", href="/page-2", active="exact"),
                dbc.NavLink("Line Chart", href="/page-3", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

# Set app layout
app.layout = html.Div([dcc.Location(id="url"), sidebar, content],style={'background-color':'#000'})


@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/page-1":
        return html.Div(
    [
    html.Div([
        html.H1('Choropleth', style={'text-align': 'center'}),
        html.Div('Select Dataset:', style={'padding': '10px','font-weight': 'bold'}),
        datasets_dropdown,
        dcc.Graph(id='choropleth-map', style={'width': '100%', 'height': '80vh'})
        ])
    ])


    elif pathname == "/page-2":
         return html.Div(
             [html.Div([
       html.H1('Bar Chart', style={'text-align': 'center'}),
       html.Div([
    html.Div([
        html.Div('Select a Dataset:', style={'padding': '10px', 'display': 'inline-block','font-weight': 'bold'}),
        datasets_dropdown,
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        html.Div('Select Country:', style={'padding': '10px', 'display': 'inline-block', 'font-weight': 'bold'}),
        dbc.Select(
            id='country-dropdown',
            value='Australia',
            style={'width': '100%', 'display': 'inline-block', 'margin-left': '10px','background-color': '#333', 'color': '#fff'}
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),
], style={'width': '100%'}),
       dcc.Graph(id='bar-chart', style={'width': '100%', 'height': '80vh'})
       ])
   ])
     
    elif pathname == "/page-3":
        return html.Div([
            html.H1('Line Chart', style={'text-align': 'center'}),
        html.Div([
    html.Div([
        html.Div('Select a Dataset:', style={'padding': '10px', 'font-weight': 'bold'}),
        datasets_dropdown,
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        html.Div('Select Countries:', style={'padding': '10px', 'font-weight': 'bold'}),
        dcc.Dropdown(
            id='country-dropdown',
            multi=True,
            value=['Australia', "United States", "New Zealand"],
            style={'width': '100%', 'display': 'inline-block','backgroundColor': '#333', 'color':"#000", 'border-radius': '10px', 'height': '36px', 'border': '1px solid #333'}
        ),
    ], style={'width': '48%', 'display': 'inline-block', 'margin-left':'10px'}),
], style={'width': '100%','display':'flex'}),

        dcc.Graph(id='line-chart', style={'width': '100%', 'height': '80vh'})
    ]) 

    elif pathname == "/":
        return home_layout
    
    else:
        # If the user tries to reach a different page, return a 404 message
        return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )
@app.callback(
    dash.dependencies.Output('choropleth-map', 'figure'),
    [dash.dependencies.Input('datasets-dropdown', 'value')]
)
def update_choropleth(selected_dataset):
    filtered_df = pd.read_csv("cleaned_datasets/"+selected_dataset+".csv")

    fig = px.choropleth(filtered_df,
                        locations='Country',
                        locationmode="country names",
                        color="Value",
                        animation_frame = "Year",
                        color_continuous_scale="Blues")
                        #title=f"{selected_dataset} by Country")
                        #labels={"color": "GDP"})

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ), coloraxis_colorbar=dict(
        #title=f"{selected_dataset}",
        titlefont_color="#fff",  
        tickfont_color="#fff"  
    ),
        height = 500,
        width=900,
        paper_bgcolor="#000",  
    plot_bgcolor="#000",  
    font_color="#fff"
    )

    return fig


# GDP by Country
@app.callback(
     dash.dependencies.Output('bar-chart', 'figure'),
     [dash.dependencies.Input('country-dropdown', 'value'),
      dash.dependencies.Input('datasets-dropdown', 'value'),]
 )
def display_bar_chart(selected_country,selected_dataset):
    filtered_df = pd.read_csv("cleaned_datasets/"+selected_dataset+".csv")
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]
     # Plot bar chart of selected country
    fig = px.bar(filtered_df,
                  x='Year',
                  y='Value',
                  color='Value',
                  color_continuous_scale='Blues')
 
    fig.update_layout(
        title=f"{selected_dataset} by Year in {selected_country}",
        paper_bgcolor="#000",  
        plot_bgcolor="#000",  
        font_color="#fff",  
        xaxis_title_font_color="#fff",  
        yaxis_title_font_color="#fff", 
        #xaxis_tick_font_color="#fff",  
        #yaxis_tick_font_color="#fff",
        yaxis_gridcolor="rgba(255, 255, 255, 0.2)"
        )
    return fig

@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('country-dropdown', 'value'),
     dash.dependencies.Input('datasets-dropdown', 'value')]
)
def display_line_chart(selected_countries, selected_dataset):
    filtered_df = pd.read_csv("cleaned_datasets/" + selected_dataset + ".csv")
    filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]

    color_discrete_sequence = px.colors.sequential.Blues[::2][::-1]
    # Plot line chart for selected countries
    fig = px.line(filtered_df, x='Year', y='Value', color='Country',
                  labels={'Value': selected_dataset},
                  title=f"{selected_dataset} by Year for Selected Countries",
                  color_discrete_sequence=color_discrete_sequence)
    
    fig.update_layout(
        paper_bgcolor="#000",  
        plot_bgcolor="#000",  
        font_color="#fff",  
        xaxis_title_font_color="#fff",  
        yaxis_title_font_color="#fff",  
       xaxis_gridcolor="rgba(255, 255, 255, 0.2)",
       yaxis_gridcolor="rgba(255, 255, 255, 0.2)"
    )
        
    return fig

# if __name__ == "__main__":
#     app.run_server(debug=True)




