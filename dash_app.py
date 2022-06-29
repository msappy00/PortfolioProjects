# Run this app with `python dash_app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import sqlite3
from dash import Dash, dash_table
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

conn = sqlite3.connect("covid.db")
df = pd.read_sql_query("SELECT Location, date, total_cases, total_deaths, "
                       "Cast(total_deaths AS REAL) / total_cases * 100 as death_percentage "
                       "FROM CovidDeaths "
                       "WHERE location == 'United States' "
                       " order by 1, 2", conn)
conn.close()

# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

app.layout = dash_table.DataTable(
        df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

if __name__ == '__main__':
    app.run_server(debug=True)
