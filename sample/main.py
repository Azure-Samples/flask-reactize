
import os

from flask import Flask

from flask_reactize import FlaskReactize


if ("MODE" not in os.environ):
    raise ValueError("You need to specify a MODE environment variable (dev or prod).")

mode = os.environ["MODE"]

proxy_api = {
    "/reqres": "https://reqres.in/api"
}

if (mode == "prod"):
    app = Flask(__name__)
    FlaskReactize(app).serve_static(
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
        proxy_api=proxy_api
    )
elif (mode == "dev"):
    app = Flask(__name__, root_path="react_app")

    FlaskReactize(app).serve_react_app(
        os.path.join(os.path.dirname(__file__), "react_app"),
        proxy_api=proxy_api
    )
else:
    raise ValueError("MODE environment variable muse be either 'dev' or 'prod'.")
