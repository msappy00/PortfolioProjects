# Run this app with `python dash_app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import sqlite3
from dash import Dash, dash_table, html
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

conn = sqlite3.connect("covid.db")
df = pd.read_sql_query("Select SUM(new_cases) as total_cases, "
                       "SUM(cast(new_deaths as REAL)) as total_deaths, "
                       "SUM(cast(new_deaths as REAL))/SUM(New_Cases)*100 as death_percentage "
                       "From CovidDeaths "
                       "where continent is not null "
                       "order by 1,2", conn)
conn.close()

df['total_cases'] = df['total_cases'].astype(int).map('{:,d}'.format)
df['total_deaths'] = df['total_deaths'].astype(int).map('{:,d}'.format)
df['death_percentage'] = df['death_percentage'].map("{:.2f}".format)

df.rename(columns={'total_cases': 'total cases',
                   'total_deaths': 'total deaths',
                   'death_percentage': 'death percentage'
                   }, inplace=True)

app.layout = html.Div(children=[dash_table.DataTable(
    df.to_dict('records'),
    columns=[{"name": i, "id": i} for i in df.columns],
    style_cell={'textAlign': 'center'},
    style_header={
        'backgroundColor': '#008000',
        'fontWeight': 'bold'
    },
    style_data={
        'color': '#000000',
        'backgroundColor': '#d3d3d3'
    }
)
])

if __name__ == '__main__':
    app.run_server(debug=True)
