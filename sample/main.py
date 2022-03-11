
import os

from flask import Flask

from flask_reactize import FlaskReactize


if ("MODE" not in os.environ):
    raise ValueError("You need to specify a MODE environment variable (dev or prod).")

mode = os.environ["MODE"]

app = Flask(__name__)

proxy_api = {
    "/reqres": "https://reqres.in/api"
}

if (mode == "prod"):
    FlaskReactize(app).serve_static(
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
        proxy_api=proxy_api
    )
elif (mode == "dev"):
    FlaskReactize(app).serve_react_app(
        os.path.join(os.path.dirname(__file__), "react_app"),
        proxy_api=proxy_api
    )
else:
    raise ValueError("MODE environment variable muse be either 'dev' or 'prod'.")
