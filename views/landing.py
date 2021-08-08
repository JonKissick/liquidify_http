import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from app import app
from dash.dependencies import Input, Output, State
from contracts_mgt import add_email
from dash import callback_context
import re
import os
import json
import boto3

if os.environ.get('AWS_KEY') == None:

    aws_id = os.getenv('AWS_KEY_IAM_DATA')
    aws_secret = os.getenv('AWS_SECRET_IAM_DATA')

    client = boto3.client('secretsmanager',
    aws_access_key_id=aws_id,
    aws_secret_access_key=aws_secret,
    region_name = 'ap-southeast-2')


else:

    secrets_client = boto3.client('secretsmanager')

    secret_arn = os.getenv('SECRET_ARN')
    id_arn = os.getenv('ID_ARN')

    auth_token = json.loads(secrets_client.get_secret_value(SecretId=secret_arn).get('SecretString'))

    rds_creds = json.loads(secrets_client.get_secret_value(SecretId=auth_token["HORSE_ARN"]).get('SecretString'))

    IAM_token = json.loads(secrets_client.get_secret_value(SecretId=id_arn).get('SecretString'))
    aws_id = IAM_token.get('aws_key')
    aws_secret = IAM_token.get('aws_secret')


############# Static Page

layout = dbc.Container([
    html.Br(),
    dbc.Container([
        html.Div([
            dbc.Container(dbc.Col(dbc.Row(
                html.Img(src='assets/website_logo.png',
                    className = 'center', style={"height" : "50%", "width" : "50%", 'textAlign': 'center'}
                     ), justify="center", align="center", className="h-50")))],style={'background-color': '#e3e2e8'})

    ]),
html.Br(),
dbc.Container(id='loginType', children=[
dbc.Row([dbc.Col([
html.H6('Contact us or leave your email to take the plunge!')])],className = 'center', style={'textAlign': 'center'}),
html.Br(),
dbc.Row([dbc.Col([
html.H4('Open@liquidify.info')])],className = 'center', style={'textAlign': 'center'}),
html.Br(),
    dbc.Row([dbc.Col(),
        dbc.Col([dbc.Input(
                type="email", id="email-input", placeholder="Your Email"),
html.Br(),
        html.Div(id='Button', children=[dbc.Button("Take the Plunge!",id='plunge-button', color="primary")])]),
    dbc.Col()],
              className = 'center', style={'textAlign': 'center'}),
    html.Br()
    #de.Lottie(options=options, width="25%", height="25%", url="/loader1"),
    ]),
])


@app.callback(Output('Button', 'children'),

              [Input('plunge-button', 'n_clicks'),
               Input('email-input', 'n_submit')
              ],

              state=
              [State('pageContent', 'children'),
              State('email-input', 'value')])


def createContract(n_clicks, email_submit,pageContent, email): # must be in same order as state

    if None == True:
        pass
    trigger = callback_context.triggered[0]
    input = re.findall(r'\d+', trigger["prop_id"].split(".")[0])
    print(input)
    clicks = callback_context.triggered[0]["value"] #n_clicks value
    print(clicks)

    if(clicks ==1):
        add_email(email)

        client = boto3.client('ses',
                              aws_access_key_id=aws_id,
                              aws_secret_access_key=aws_secret,
                              region_name='ap-southeast-2')

        response = client.send_email(
            Destination={
                'ToAddresses': [
                    str(email)
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': "<h1>Plunge Taken!</h1><p>Hey there,</p><p>Thanks for registering your interest in Liquidify.</p><p>We're excited that you want to come with us on a journey to open data which will enable communities to solve the problems of tomorrow.</p><p>We'll be in contact with you shortly.</p><p>In the mean-time, feel free to explore the website or contact us at Open@liquidify.info</p><p>All the best from the Liquidify team</p>",
                    },
                    # 'Text': {
                    #     'Charset': 'UTF-8',
                    #     'Data': 'This is for those who cannot read HTML.',
                    # },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'Liquidify - Plunge Taken',
                },
            },
            Source='open@liquidify.info',
        )

    if(clicks > 0):

        return(dbc.Button("Plunge Taken!",outline=True, id='plunge-button', color="success", disabled=True))

    else:
        return(dbc.Button("Take the Plunge!",id='plunge-button', color="primary"))