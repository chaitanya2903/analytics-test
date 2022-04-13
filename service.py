import pandas as pd
import sqlite3
import json
import plotly.express as px
import plotly
import plotly.graph_objects as go


def create_db():
    files = os.listdir()
    df = pd.read_csv('moody2022_new.csv')

    con = sqlite3.connect('moody.sqlite')
    df.to_sql('moody', con, if_exists='append', index=False)
    con.close()


def get_figure():
    con = sqlite3.connect('moody.sqlite')
    df = pd.read_sql_query('select * from moody', con)
    con.close()
    df.sort_values(by='GRADE', inplace=True)
    fig = px.box(df, x='GRADE', y='SCORE',
                 color='GRADE', width=900, height=700)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return {'data': df, 'figure': graphJSON}


def execute_query(query):
    con = sqlite3.connect('moody.sqlite')

    results = get_figure()

    df1 = results['data']
    df2 = pd.read_sql_query(query, con)
    # df = pd.concat([df1, df2])
    # df = pd.melt(df,id_vars= ['Location'], var_name= ['GRADE'])
    con.close()

    fig = go.Figure()
    fig.add_trace(
        go.Box(x=df1.GRADE,
               y=df1.SCORE,
               name = 'Plot Zero')
    )
    fig.add_trace(
        go.Box(
            x=df2.GRADE,
            y=df2.SCORE,
            name = 'Sliced Plot'
        )
    )
    fig.update_layout(
        boxmode='group',
        width = 900,
        height = 700
    )

    # fig = px.box(df, x = 'Location', y = 'value', color = 'GRADE', width = 900, height = 700)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return {'figure1': graphJSON, 'data': results['data']}
