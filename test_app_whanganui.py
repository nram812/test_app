import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import flask
dirs = r"nzens_probs_2020072303_utc_1H_sum_rain_amount_accumulation.xlsx"
df = pd.read_excel(dirs, index_col =[0,1])

mgr_options = df.index.droplevel(1).unique().values#df["Manager"].unique()

dirs3 = r"nzens_probs_2020072303_utc_24H_sum_rain_amount_accumulation.xlsx"
df3 = pd.read_excel(dirs3, index_col =[0,1])
mgr_options3 = df3.index.droplevel(1).unique().values#


dirs2 = r"nzens_probs_2020072303_utc_6H_sum_rain_amount_accumulation.xlsx"
df2 = pd.read_excel(dirs2, index_col =[0,1])
mgr_options2 = df2.index.droplevel(1).unique().values#



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
frequency = dirs.split('_')[4]


server = flask.Flask(__name__) 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)
#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True
app.layout = html.Div([
    html.H2("Probability of 1,6 and 24H Rainfall Exceeding Thresholds in Whanganui"),
    html.Div(
        [
            dcc.Dropdown(
                id="1H",
                options=[{
                    'label': i,
                    'value': i
                } for i in mgr_options],
                value=mgr_options),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='code-graph'),
    html.Div(
    [
        dcc.Dropdown(
            id="12H",
            options=[{
                'label': i,
                'value': i
            } for i in mgr_options2],
            value=mgr_options2),
    ],
    style={'width': '25%',
           'display': 'inline-block'}),
dcc.Graph(id='funnel-graph'),
html.Div(
    [
        dcc.Dropdown(
            id="24H",
            options=[{
                'label': i,
                'value': i
            } for i in mgr_options3],
            value=mgr_options3),
    ],
    style={'width': '25%',
           'display': 'inline-block'}),
dcc.Graph(id='funnel2-graph')
])


@app.callback(
    dash.dependencies.Output('code-graph', 'figure'),
    [dash.dependencies.Input('1H', 'value')])
def update_graph(Manager):
    if Manager == "All Managers":
        df_plot = df.copy()
    else:
        df_plot = df.loc[Manager]['Probability of Exceeding Threshold (%) ']#[df['Manager'] == Manager]

    # pv = pd.pivot_table(
    #     df_plot,
    #     index=['Name'],
    #     columns=["Status"],
    #     values=['Quantity'],
    #     aggfunc=sum,
    #     fill_value=0)

    trace1 = go.Line(x=df_plot.index, y=df_plot.values.ravel(), name ='Probability of Exceeding Threshold (%) ')
    # trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pending')], name='Pending')
    # trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presented')], name='Presented')
    # trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'won')], name='Won')

    return {
        'data': [trace1],
        'layout':
        go.Layout(
            title='Probability of Rainfall Exceeding {} mm'.format(Manager),
            barmode='stack')
    }



@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('12H', 'value')])
def update_graph(Manager):
    if Manager == "All Managers":
        df_plot = df2.copy()
    else:
        df_plot = df2.loc[Manager]['Probability of Exceeding Threshold (%) ']#[df['Manager'] == Manager]

    # pv = pd.pivot_table(
    #     df_plot,
    #     index=['Name'],
    #     columns=["Status"],
    #     values=['Quantity'],
    #     aggfunc=sum,
    #     fill_value=0)

    trace1 = go.Line(x=df_plot.index, y=df_plot.values.ravel(), name ='Probability of Exceeding Threshold (%) ')
    # trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pending')], name='Pending')
    # trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presented')], name='Presented')
    # trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'won')], name='Won')

    return {
        'data': [trace1],
        'layout':
        go.Layout(
            title='Probability of 6H Rainfall Exceeding {} mm'.format(Manager),
            barmode='stack')
    }

@app.callback(
    dash.dependencies.Output('funnel2-graph', 'figure'),
    [dash.dependencies.Input('24H', 'value')])
def update_graph(Manager):
    if Manager == "All Managers":
        df_plot = df3.copy()
    else:
        df_plot = df3.loc[Manager]['Probability of Exceeding Threshold (%) ']#[df['Manager'] == Manager]

    # pv = pd.pivot_table(
    #     df_plot,
    #     index=['Name'],
    #     columns=["Status"],
    #     values=['Quantity'],
    #     aggfunc=sum,
    #     fill_value=0)

    trace1 = go.Line(x=df_plot.index, y=df_plot.values.ravel(), name ='Probability of Exceeding Threshold (%) ')
    # trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pending')], name='Pending')
    # trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presented')], name='Presented')
    # trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'won')], name='Won')

    return {
        'data': [trace1],
        'layout':
        go.Layout(
            title='Probability 24 H of Rainfall Exceeding {} mm'.format(Manager),
            barmode='stack')
    }



if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8888,debug=True)
