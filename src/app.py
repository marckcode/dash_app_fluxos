import pandas as pd

import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

df1_pw25 = pd.read_csv('data/202610_PWF25_V2A2F2_REV2.csv')
df1_pw25['XING_TOT'] = df1_pw25['XESTR_MW'] + df1_pw25['XTRIO_MW']
df1_pw16 = pd.read_csv('data/202610_PWF16_V2A2F2_REV2.csv')
df1_total = pd.concat([df1_pw16, df1_pw25.iloc[:, 2:]], axis=1)
df1_total.name = 'V2A2F2_REV2'

df2_pw25 = pd.read_csv('data/202610_PWF25_V2A2F5_REV1.csv')
df2_pw25['XING_TOT'] = df2_pw25['XESTR_MW'] + df2_pw25['XTRIO_MW']
df2_pw16 = pd.read_csv('data/202610_PWF16_V2A2F5_REV1.csv')
df2_total = pd.concat([df2_pw16, df2_pw25.iloc[:, 2:]], axis=1)
df2_total.name = 'V2A2F5_REV1'

df3_pw25 = pd.read_csv('data/202610_PWF25_V1A1F2_REV1.csv')
df3_pw25['XING_TOT'] = df3_pw25['XESTR_MW'] + df3_pw25['XTRIO_MW']
df3_pw16 = pd.read_csv('data/202610_PWF16_V1A1F2_REV1.csv')
df3_total = pd.concat([df3_pw16, df3_pw25.iloc[:, 2:]], axis=1)
df3_total.name = 'V1A1F2_REV1'

df4_pw25 = pd.read_csv('data/202610_PWF25_V1A1F4_REV1.csv')
df4_pw25['XING_TOT'] = df4_pw25['XESTR_MW'] + df4_pw25['XTRIO_MW']
df4_pw16 = pd.read_csv('data/202610_PWF16_V1A1F4_REV1.csv')
df4_total = pd.concat([df4_pw16, df4_pw25.iloc[:, 2:]], axis=1)
df4_total.name = 'V1A1F4_REV1'

df5_pw25 = pd.read_csv('data/202610_PWF25_V1A1F5_REV1.csv')
df5_pw25['XING_TOT'] = df5_pw25['XESTR_MW'] + df5_pw25['XTRIO_MW']
df5_pw16 = pd.read_csv('data/202610_PWF16_V1A1F5_REV1.csv')
df5_total = pd.concat([df5_pw16, df5_pw25.iloc[:, 2:]], axis=1)
df5_total.name = 'V1A1F5_REV1'

df6_pw25 = pd.read_csv('data/202610_PWF25_V2A2F3_REV1.csv')
df6_pw25['XING_TOT'] = df6_pw25['XESTR_MW'] + df6_pw25['XTRIO_MW']
df6_pw16 = pd.read_csv('data/202610_PWF16_V2A2F3_REV1.csv')
df6_total = pd.concat([df6_pw16, df6_pw25.iloc[:, 2:]], axis=1)
df6_total.name = 'V2A2F3_REV1'

df7_pw25 = pd.read_csv('data/202610_PWF25_V2A2F4_REV1.csv')
df7_pw25['XING_TOT'] = df7_pw25['XESTR_MW'] + df7_pw25['XTRIO_MW']
df7_pw16 = pd.read_csv('data/202610_PWF16_V2A2F4_REV1.csv')
df7_total = pd.concat([df7_pw16, df7_pw25.iloc[:, 2:]], axis=1)
df7_total.name = 'V2A2F4_REV1'

dict_main = {'V2A2F2_REV2': df1_total.iloc[:, 2:], 'V2A2F5_REV1': df2_total.iloc[:, 2:],
             'V1A1F2_REV1': df3_total.iloc[:, 2:], 'V1A1F4_REV1': df4_total.iloc[:, 2:],
             'V1A1F5_REV1': df5_total.iloc[:, 2:], 'V2A2F3_REV1': df6_total.iloc[:, 2:],
             'V2A2F4_REV1': df7_total.iloc[:, 2:]}

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Source+Code+Pro:ital,wght@0,200..900;1,200..900&display=swap"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

rpm = list(dict_main.keys())
channels = dict_main[rpm[0]]



app.layout = html.Div(
    [
        html.Div([
        dcc.Dropdown(
            id='rpm-dropdown',
            options=[{'label':speed, 'value':speed} for speed in rpm],
            value=list(dict_main.keys())[0],
            # I removed the multi=True because it requires a distinction between the columns in the next dropdown...
            searchable=False
            ),
            ],style={'width': '20%', 'display': 'inline-block'}),
        html.Div([
        dcc.Dropdown(
            id='channel-dropdown',
            multi=True
            ),
            ],style={'width': '20%', 'display': 'inline-block'}
        ),
		html.Div([
			dcc.Graph(
				id='Main-Graph' # the initial graph is in the callback
			),
			], style={'width': '98%', 'display': 'inline-block'}
		)
    ]
)



@app.callback(
    Output('channel-dropdown', 'options'),
    [Input('rpm-dropdown', 'value')])
def update_date_dropdown(speed):
    #print([i for i in dict_main[speed]])
    data_value = [{'label': i, 'value': i} for i in dict_main[speed]]
    return data_value

@app.callback(
    Output('Main-Graph', 'figure'),
    [Input('channel-dropdown', 'value')],
    [State('rpm-dropdown', 'value')]) # This is the way to inform the callback which dataframe is to be charted
def updateGraph(channels, speed):
    if channels:
        # print(speed)
        fig = go.Figure(data=[go.Scatter(x=dict_main[speed].index, y=dict_main[speed][i]) for i in channels])
        fig.update_layout(
            margin=dict(t=50, b=2),
            autosize=True,
            xaxis=dict(title_text="Dia", tickangle=-45),
            yaxis=dict(title_text="Active Power (MW)"),
            height=560
        )
        fig.update_layout(
            title=dict(text=speed, font=dict(size=35), automargin=True, yref='paper')
        )
        return fig
    else:
        return go.Figure(data=[])
    
    
	
if __name__ == '__main__':
	app.run_server(debug=True)