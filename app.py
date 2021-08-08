import dash
import os
from config import config
from flask import send_from_directory

external_css = [
    "https://negomi.github.io/react-burger-menu/example.css",
    "https://negomi.github.io/react-burger-menu/normalize.css",
    "https://negomi.github.io/react-burger-menu/fonts/font-awesome-4.2.0/css/font-awesome.min.css"
]

app = dash.Dash(__name__, external_stylesheets=external_css)
server = app.server
app.config.suppress_callback_exceptions = True


# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=config.get('database', 'con'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)


#################################################
########## ADD LOTTIE ANIMATIONS ################
#################################################
#
# @server.route("/loader1", methods=["GET"])
# def serving_lottie_loader1():
#     directory = os.path.join(os.getcwd(), "assets/lottie")
#     return send_from_directory(directory,"windfarm.json")
#
# @server.route("/loader2", methods=["GET"])
# def serving_lottie_loader2():
#     directory = os.path.join(os.getcwd(), "assets/lottie")
#     return send_from_directory(directory,"car_charge.json")
#
# @server.route("/loader3", methods=["GET"])
# def serving_lottie_loader3():
#     directory = os.path.join(os.getcwd(), "assets/lottie")
#     return send_from_directory(directory,"solar.json")