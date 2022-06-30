# Run this app with `python dash_app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import sqlite3
from dash import Dash, dash_table, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

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
df2 = pd.read_sql_query("Select location, SUM(cast(new_deaths as int)) as total_death_count "
                        "From CovidDeaths "
                        "Where continent is null "
                        "and location not in ('World', 'European Union', 'International', "
                        "'High income', 'Upper middle income', 'Lower middle income', 'Low income') "
                        "Group by location "
                        "order by total_death_count desc", conn)

conn.close()

df2.rename(columns={'total_death_count': 'total death count',
                    'location': 'continent'}, inplace=True)

fig = px.bar(df2, x='continent', y='total death count', color='continent')
# title='<b>Total Death Count by Continent</b>'

fig.update(layout_showlegend=False)

app.layout = html.Div(children=[

    html.H2(children='Global Numbers'),

    dash_table.DataTable(
        df1.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df1.columns],
        style_cell={'textAlign': 'center'},
        style_header={
            'backgroundColor': '#008000',
            'fontWeight': 'bold'
        },
        style_data={
            'color': '#000000',
            'backgroundColor': '#d3d3d3'
        }
    ),

    html.H2(children='Total Death Count by Continent'),

    dcc.Graph(
        id='my_graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
