import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(
        children='Bill Splitter and Tip Calculator',
        style={'text-align': 'center'}
    ),
    html.Div([
        html.P([
            html.Label('Enter bill amount: '),
            dcc.Input(value='0', type='number', id='bill')
        ,
            html.Label('How much would you like to tip? '),
            dcc.Slider(
                min=10,
                max=20,
                marks={
                    10: '10%',
                    11: '11%',
                    12: '12%',
                    13: '13%',
                    14: '14%',
                    15: '15%',
                    16: '16%',
                    17: '17%',
                    18: '18%',
                    19: '19%',
                    20: '20%',
                },
                value=15,
                id='slide'
            )
        ,
            html.Br([]),
            html.Br([]),

            html.Label('OR Enter other percentage tip: '),
            dcc.Input(value='0', type='number', id='tip')
            ,
            html.Label('OR Enter flat tip amount: '),
            dcc.Input(value='0', type='number', id='flattip'),

            html.Label('How many people are splitting the bill?'),
            dcc.Input(value='0', type='number', id='amtofppl')
        ], style={'columnCount': 2}
        )
    ]),
    html.Div([html.Br()]),
    html.Div([
        html.P([
            html.Label('Tip amount by Person: '),
            html.H6(id='tipaid'),

            html.Label('Total Tip Amount: '),
            html.H6(id='totaltip'),

            html.Label('Total Amount Paid: '),
            html.H6(id='tots'),

            html.Label('Amount per person: '),
            html.H6(id='amt')
        ], style={'columnCount': 2, 'text-align': 'left'}
        )
    ]),

    html.Div([
        html.P([
            html.H6('Amount paid per person'),
            dcc.Graph(id='graphpp'),
            html.H6('Total paid'),
            dcc.Graph(id='graphtotal')
        ], style={'columnCount': 2}),
    ])
    ]
)

@app.callback(
    Output('graphpp', 'figure'), Output('graphtotal', 'figure'), Output('totaltip', 'children'), Output('tipaid', 'children'), Output('amt', 'children'), Output('tots','children'), Input('slide', 'value'), Input('bill', 'value'), Input('tip', 'value'), Input('flattip', 'value'), Input('amtofppl', 'value')
)
def calculate_tip(slide, bill, tip, flattip, amtofppl):
    bill = float(bill)

    while bill>0 and bill!=None:
        tipamt = 0
        slide = float(slide)
        flattip = float(flattip)
        amtofppl = float(amtofppl)

        tip = float(tip)

        if slide != 0:
            tipamt = slide/100*bill
        if tip != 0:
            tipamt = tip/100*bill

        if flattip != 0:
            tipamt = flattip

        totalamt = round(bill+tipamt, 2)
        totaltip = round(tipamt, 2)


        tipamt = round(tipamt, 2)

        fig2 = go.Figure(data=[
            go.Bar(name='Total Bill Amount', y=[bill], x=[1], text=bill, textposition='auto'),
            go.Bar(name='Total Tip Amount', y=[totaltip], x=[1], text=totalamt, textposition='outside')
        ])
        fig2.update_layout(barmode='stack')

        totaltip = "${:.2f}".format(totaltip)

        if amtofppl < 2:
            totalamt = "${:.2f}".format(totalamt)
            tipamt = "${:.2f}".format(tipamt)
            return fig2, fig2, totaltip, tipamt, totalamt, totalamt
        else:
            tipamt = tipamt/amtofppl
            totalamt2 = round(totalamt/amtofppl, 2)

            fig1 = go.Figure(data=[
                go.Bar(name='Bill Per Person', y=[bill / amtofppl], x=[1], text="${:.2f}".format(totalamt),
                       textposition='outside'),
                go.Bar(name='Tip Per Person', y=[tipamt], x=[1], text="${:.2f}".format(tipamt), textposition='auto')
            ])
            fig1.update_layout(barmode='stack')

            tipamt = "${:.2f}".format(tipamt)
            totalamt = "${:.2f}".format(totalamt)
            totalamt2 = "${:.2f}".format(totalamt2)

            return fig1, fig2, totaltip, tipamt, totalamt2, totalamt
    fig1 = go.Figure([])
    fig2 = go.Figure([])
    return fig1, fig2, 0, 0, 0, 0

if __name__ == "__main__":
    app.run_server(debug=True)

