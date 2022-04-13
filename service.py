import pandas as pd
import sqlite3
import json
import plotly.express as px
import plotly

def create_db():
    files = os.listdir()
    df = pd.read_csv('moody2022_new.csv')
    
    con = sqlite3.connect('moody.sqlite')
    df.to_sql('moody', con, if_exists = 'append', index = False)
    con.close()

def get_figure():
    con = sqlite3.connect('moody.sqlite')
    df = pd.read_sql_query('select * from moody', con)
    con.close()
    df.sort_values(by = 'GRADE', inplace = True)
    fig = px.box(df, x = 'GRADE', y = 'SCORE', color = 'GRADE', width = 900, height = 700)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return {'data' : df, 'figure': graphJSON}

def execute_query(query):
    con = sqlite3.connect('moody.sqlite')
    
    df = pd.read_sql_query(query, con)
    con.close()
    df.sort_values(by = 'GRADE', inplace = True)
    fig = px.box(df, x = 'GRADE', y = 'SCORE', color = 'GRADE', width = 900, height = 700)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    results = get_figure()

    return {'figure1': graphJSON,'figure2': results['figure'] , 'data': results['data']}


