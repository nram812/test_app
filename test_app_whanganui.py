import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import flask

df = pd.read_excel(r"nzens_probs_2020072303_utc_6H_sum_rain_amount_accumulation.xlsx", index_col =[0,1])

mgr_options = df.index.droplevel(1).unique().values#df["Manager"].unique()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__) 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)
#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True
app.layout = html.Div([
    html.H2("Probability of Rainfall Exceeding Value in Whanganui"),
    html.Div(
        [
            dcc.Dropdown(
                id="Thresholds",
                options=[{
                    'label': i,
                    'value': i
                } for i in mgr_options],
                value=mgr_options),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph'),
])


@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('Thresholds', 'value')])
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


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8888,debug=True)
