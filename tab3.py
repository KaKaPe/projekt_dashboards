import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go


def render_tab(df):

    df['weekday'] = df['tran_date'].dt.weekday
    grouped = df[df['total_amt'] > 0].groupby([pd.Grouper(key='weekday'),
                                               'Store_type'])['total_amt'].mean().round(2).unstack()

    traces = []
    for col in grouped.columns:
        values = grouped[col].tolist()
        traces.append(values)

    fig = go.Figure(data=go.Heatmap(z=traces,
                                    x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sutarday', 'Sunday'],
                                    y=grouped.columns, hoverongaps=False),
                    layout=go.Layout(title='Sprzedaż w kanałach według dni tygodnia'))

    layout = html.Div([html.H1('Kanały Sprzedaży',
                               style={'text-align': 'center'}),
                       html.Div([html.Div([dcc.Graph(id='heatmap-store-type', figure=fig)],
                                          style={'width': '50%'}),
                                 html.Div([dcc.Dropdown(
                                     id='store-type-dropdown',
                                     options=[{'label': store_type, 'value': store_type} for store_type in df['Store_type'].unique()],
                                     value=df['prod_cat'].unique()[0]
                                 ),
                                          dcc.Graph(id='violin-customer-demography')],
                                          style={'width': '50%'})], style={'display': 'flex'}),
                       html.Div(id='temp-out')
                       ])

    return layout
