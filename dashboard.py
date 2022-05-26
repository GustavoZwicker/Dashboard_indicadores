from cProfile import label
from dash import Dash, dcc, html, Input, Output
from matplotlib.pyplot import legend, xlabel
from numpy import sort
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.ExcelFile('inteligente-dados-sn.xlsx')
df = pd.read_excel(df, 'DadosEscolhidos')
x = df.Estado.unique()
y = df['População total estimada do município'].groupby(df['Estado']).sum()
fig = px.bar(df, x=x, y=y, color=y, barmode="group")

app.layout = html.Div(children=[
    dcc.Graph(
        id='graph1',
        
    ),
    
    dcc.Graph(
        id='graph2',
    ),

    html.Div(
        html.Table([
        html.Tr([html.Td(['Média']), html.Td(id='mean')]),
        html.Tr([html.Td(['Desvio Padrão']), html.Td(id='std')]),
        html.Tr([html.Td(['Valor Mínimo']), html.Td(id='min')]),
        html.Tr([html.Td(['25%']), html.Td(id='quantile25')]),
        html.Tr([html.Td(['50%']), html.Td(id='quantile50')]),
        html.Tr([html.Td(['75%']), html.Td(id='quantile75')]),
        html.Tr([html.Td(['Valor Máximo']), html.Td(id='max')]),
    ]),
        ),
    dcc.Dropdown(df.columns[:3], df.columns[1], id='Filter-dropdown'),
    dcc.Dropdown(df.columns[3:], df.columns[4], id='Y-Axis-dropdown'),
    
    dcc.Dropdown(options={
        'category ascending' : 'Alfabética',
        'total ascending' : 'Crescente',
        'total descending' : 'Decrescente',
        }, value='category ascending', id='Sort-dropdown')
])

@app.callback(
    Output('graph1', 'figure'),
    Input('Y-Axis-dropdown', 'value'),
    Input('Filter-dropdown', 'value'),
    Input('Sort-dropdown', 'value')
)
def update_graph1(value, filter_value, sort_as):
    x = df[filter_value].unique()
    y = df[value].groupby(df[filter_value]).sum()
    fig = px.bar(df, x=x, y=y, color=y, barmode="group", labels= {'x':value, 'y':filter_value})
    fig.update_xaxes(categoryorder=sort_as)
    return fig

@app.callback(
    Output('graph2', 'figure'),
    Input('Y-Axis-dropdown', 'value'),
    Input('Filter-dropdown', 'value'),
    Input('Sort-dropdown', 'value')
)
def update_graph2(value, filter_value, sort_as):
    x = df[filter_value].unique()
    y = df[value].groupby(df[filter_value]).mean()
    average = df[value].groupby(df[filter_value]).mean().mean()
    fig = px.scatter(df, x=x, y=y, color=y, labels= {'x':value, 'y':filter_value})
    fig.update_xaxes(categoryorder=sort_as)
    fig.add_shape(
    type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=average, y1=average, yref="y")
    return fig

@app.callback(
    Output('mean', 'children'),
    Output('std', 'children'),
    Output('min', 'children'),
    Output('quantile25', 'children'),
    Output('quantile50', 'children'),
    Output('quantile75', 'children'),
    Output('max', 'children'),
    Input('Y-Axis-dropdown', 'value'),
    Input('Filter-dropdown', 'value'),
    Input('Sort-dropdown', 'value')
)
def describe_data(value, filter_value, sort_as):
    y = df[[value]].groupby(df[filter_value]).mean()
    
    return y.mean(), y.std(), y.min(), y.quantile(q=0.25), y.quantile(q=0.5), y.quantile(q=0.75), y.max()

if __name__ == '__main__':
    app.run_server(debug=True)