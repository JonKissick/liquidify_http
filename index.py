# index page

#### so change the database config but where?
import os

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
#import dash_extensions as de
#from dash_extensions import Burger
from app import app, server
from flask_login import logout_user, current_user
from views import landing

print(os.getcwd())

# Lottie Setup options.
#options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

# Link image and text
def link_element(icon, text):
    return html.A(children=[html.I(className=icon), html.Span(text)], href=f"/{text}",  #### Could be this!!!!!
                  className="bm-item", style={"display": "block"})

# navBar = Burger(children=[
#         html.Nav(children=[
#             html.Br(),
#             link_element("fa fa-fw fa-globe", "Home"),
#             link_element("fa fa-fw fa-bar-chart", "Data"),
#         ], className="bm-item-list", style={"height": "100%"})
#     ], effect="bubble")

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        #navBar,
        html.Div(id='pageContent')
    ])
], id='table-wrapper')


################################################################################
# HANDLE PAGE ROUTING - IF USER NOT LOGGED IN, ALWAYS RETURN TO LOGIN SCREEN
################################################################################
@app.callback(Output('pageContent', 'children'),
              [Input('url', 'pathname')])   ###### If user is authenticated, send to current deals
def displayPage(pathname):
    if pathname == '/':
            return landing.layout


    elif pathname == '/Home':
            return landing.layout

    elif pathname == '/Data':
            return landing.layout

    # if pathname == '/admin':
    #     if current_user.is_authenticated:
    #         if current_user.admin == 0:
    #             return user_admin.layout
    #         else:
    #             return error.layout
    #     else:
    #         return login.layout
    #
    #
    # else:
    #     return error.layout


################################################################################
# ONLY SHOW NAVIGATION BAR WHEN A USER IS LOGGED IN
################################################################################
@app.callback(
    Output('navBar', 'children'),
    [Input('pageContent', 'children')])
def navBar(input1):
            navBarContents = [dbc.Nav([
                dbc.DropdownMenu(
                    nav=True,
                    in_navbar=True,
                    label="Retail Deal Capture",
                    children=[
                        dbc.DropdownMenuItem('Retail Home', href='/retail_home'),
                        dbc.DropdownMenuItem('Profile', href='/profile'),
                        dbc.DropdownMenuItem('Admin', href='/admin'),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem('Logout', href='/logout'),
                    ],style={'justify':'right'},
                ),
            ],className='navbar-nav')
            ]
            return navBarContents


if __name__ == '__main__':
    from waitress import serve

    serve(app.server, host="0.0.0.0", port=8050, threads=8)#, url_scheme = 'https')