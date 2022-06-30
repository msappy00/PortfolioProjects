# Run this app with `python dash_app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import sqlite3
from dash import Dash, dash_table, html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(__name__)

colors = {
    'background': '#ffffff',
    'text': '#00304E'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

conn = sqlite3.connect("covid.db")
df1 = pd.read_sql_query("Select SUM(new_cases) as total_cases, "
                        "SUM(cast(new_deaths as REAL)) as total_deaths, "
                        "SUM(cast(new_deaths as REAL))/SUM(New_Cases)*100 as death_percentage "
                        "From CovidDeaths "
                        "where continent is not null "
                        "order by 1,2", conn)
conn.close()

df1['total_cases'] = df1['total_cases'].astype(int).map('{:,d}'.format)
df1['total_deaths'] = df1['total_deaths'].astype(int).map('{:,d}'.format)
df1['death_percentage'] = df1['death_percentage'].map("{:.2f}".format)

df1.rename(columns={'total_cases': 'total cases',
                    'total_deaths': 'total deaths',
                    'death_percentage': 'death percentage'
                    }, inplace=True)

conn = sqlite3.connect("covid.db")
df2 = pd.read_sql_query("Select location, SUM(cast(new_deaths as REAL)) as total_death_count "
                        "From CovidDeaths "
                        "Where continent is null "
                        "and location not in ('World', 'European Union', 'International', "
                        "'High income', 'Upper middle income', 'Lower middle income', 'Low income') "
                        "Group by location "
                        "order by total_death_count desc", conn)

conn.close()

df2.rename(columns={'total_death_count': 'total death count',
                    'location': 'continent'}, inplace=True)

bar_graph_fig = px.bar(df2, x='continent', y='total death count', color='continent')
# title='<b>Total Death Count by Continent</b>'

bar_graph_fig.update(layout_showlegend=False)

conn = sqlite3.connect("covid.db")
df3 = pd.read_csv('test.csv', names=['iso_code', 'location', 'population', 'max_infected', 'percent infected'])

conn.close()

map_fig = px.choropleth(df3, locations="location",
                        color_continuous_scale='Viridis_r',
                        color="percent infected",
                        locationmode="country names",
                        title='<b>Percent Population Infected by Country</b>')
map_fig.update_layout(geo_bgcolor='lightblue')

table_spacer = html.H2(style={'height': 100})
table_title = html.H4(children='Global Numbers', style={
            'color': colors['text']
        })
table_view = dash_table.DataTable(
    df1.to_dict('records'),
    columns=[{"name": i, "id": i} for i in df1.columns],
    style_cell={'textAlign': 'center'},
    style_header={
        'color': '#ffffff',
        'backgroundColor': '#4F1E00',
        'fontWeight': 'bold'
    },
    style_data={
        'color': '#000000',
        'backgroundColor': '#d3d3d3'
    })
map_view = dcc.Graph(
    id='map_graph',
    figure=map_fig
)

bar_graph_title = html.H4(children='Total Death Count by Continent', style={
            'color': colors['text']})
bar_graph_view = dcc.Graph(
    id='bar_graph',
    figure=bar_graph_fig
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    dbc.Container([
        dbc.Row([
            dbc.Col([table_spacer, table_title, table_view], width=4),
            dbc.Col(map_view, width=8),
        ]),
        dbc.Row([
            dbc.Col([bar_graph_title, bar_graph_view], width=8)
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
