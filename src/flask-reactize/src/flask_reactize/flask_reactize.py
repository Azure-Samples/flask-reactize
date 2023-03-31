import os
from typing import Dict, Optional

import requests
from flask import Flask, Response, request, send_from_directory

from .node_wrapper import NodeWrapper
from .utils import clear_flask_default_status_rule, join_uri, rprint


class FlaskReactize:

    flask_app: Flask = None

    def __init__(self, flask_app: Flask):
        """
        Initialize a new instance of the FlaskReactize class

        :param flask_app: the Flask app to attach static web site to
        :return: None
        """

        if flask_app is None:
            raise ValueError("flask_app must be a valid Flask instance.")

        self.flask_app = flask_app

    def serve_static(
        self, static_folder: str, proxy_api: Optional[Dict] = None
    ) -> None:
        """
        Call this function to activate a react static web site
        for the given Flask application

        :param static_folder: static folder containing the compiled react site
        :param proxy_api: (dict) proxy for api. Format {"prefix": "endpoint", "other_prefix": "other_endpoint"}
        :return: None
        """

        if static_folder is None:
            raise ValueError("static_folder must be provided.")

        if not os.path.exists(static_folder):
            raise ValueError("static_folder must must be a valid folder.")

        print(static_folder)

        # Set the static
        self.flask_app.static_folder = static_folder
        self.flask_app.static_url_path = "/static"

        # Clear Flask default static route
        clear_flask_default_status_rule(self.flask_app, False)

        # If proxy_api is not empty, register routes for proxying APIs
        if proxy_api is not None:
            self.__set_proxy_api(proxy_api)

        # Set the / route for all static files
        self.flask_app.add_url_rule(
            "/",
            endpoint="/",
            view_func=lambda: self.__send_static(static_folder, ""),
            methods=["GET"],
        )

        self.flask_app.add_url_rule(
            "/<path:path>",
            defaults={"path": ""},
            endpoint="/<path:path>",
            view_func=lambda path: self.__send_static(static_folder, path),
            methods=["GET"],
        )

    def __send_static(self, static_folder: str, path: str) -> Response:
        """
        Serve a static file. It is an internal method and should not
        be called directly.
        """
        print("static_folder: " + static_folder)
        print("p: " + path)

        if path != "" and os.path.exists(static_folder + "/" + path):
            return send_from_directory(static_folder, path)
        else:
            return send_from_directory(static_folder, "index.html")

    def serve_react_app(
        self,
        source_react_folder: str,
        port: Optional[int] = 3005,
        proxy_api: Optional[Dict] = None,
    ) -> None:
        """
        Call this function to activate a react web site
        for the given Flask application

        :param source_react_folder: react source folder
        :param port: Port number to start the reac app on. Optional, default 3005
        :param proxy_api: (dict) proxy for api. Format {"prefix": "endpoint", "other_prefix": "other_endpoint"}
        :return: None
        """

        if source_react_folder is None:
            raise ValueError("static_folder must be provided.")

        if not os.path.exists(source_react_folder):
            raise ValueError("static_folder must must be a valid folder.")

        # Make sure that at the first request, the node server is started.
        # Note: there are not "startup" event, so, it is basically
        # the best place to put it :)
        self.flask_app.before_first_request(
            lambda: self.__start_react_server(source_react_folder, port)
        )

        # Clear Flask default route
        clear_flask_default_status_rule(self.flask_app, False)

        # Add the port to the React env. variable for the websocket call
        # to be routed directly to the nodejs server
        os.environ["WDS_SOCKET_PORT"] = str(port)

        # If proxy_api is not empty, register routes for proxying APIs
        if proxy_api is not None:
            self.__set_proxy_api(proxy_api)

        # Create routes to redirect HTTP requests from the python app
        # to the nodejs app, routing responses to the client
        self.flask_app.add_url_rule(
            "/",
            endpoint="/",
            defaults={"filePath": ""},
            view_func=lambda filePath: self.__route_react_http(port, filePath),
            methods=["get"],
        )

        self.flask_app.add_url_rule(
            "/<path:filePath>",
            "/<path:filePath>",
            lambda filePath: self.__route_react_http(port, filePath),
        )

    def __route_react_http(self, port: int, filePath: str) -> Response:
        """
        Serve react files by routing calls to the underlying nodejs app.
        It is an internal method and should not be called directly.
        """

        react_app_url = f"http://127.0.0.1:{port}/{filePath}"

        try:
            react_response = requests.get(react_app_url)
            react_response.raise_for_status()
            content = react_response.content

            response = Response(
                status=react_response.status_code,
                content_type=react_response.headers["Content-Type"],
            )

            response.set_data(content)
            return response
        except requests.exceptions.ConnectionError:
            rprint("Application not ready")
            return Response(status=503)
        except Exception as ex:
            rprint(f"An exception occured. The message is: {ex}")
            raise Response(status=500)

    def __react_stdout(self, proc) -> None:
        for line in iter(proc.stdout.readline, b""):
            if "You can now view" in line.decode("utf-8"):
                rprint("Application ready.")
            if "To ignore, add" in line.decode("utf-8"):
                rprint(
                    "Application ready with warnings (find React logs in the browser developer toolbar)."
                )

    def __start_react_server(self, source_react_folder: str, port: int) -> None:
        """
        Start the node server for the given path. It is an internal
        method and should not be called directly.

        :param source_react_folder: react source folder
        :return: None
        """

        node_wrapper = NodeWrapper()

        # Create the underlying nodejs server
        rprint("[Re]Starting React application (nodejs) ...")

        node_wrapper.start(
            port, source_react_folder, stdout_handler=self.__react_stdout
        )

    def __set_proxy_api(self, proxy_api: Dict) -> None:
        """
        Set the proxy API by adding rules
        """

        for prefix, endpoint in proxy_api.items():
            self.flask_app.add_url_rule(
                f"{prefix}/<path:path>",
                endpoint=f"{prefix}/<path:path>",
                view_func=lambda path: self.__serve_proxy_api(endpoint, path),
                methods=["GET", "POST", "DELETE", "PUT", "PATCH"],
            )

    def __serve_proxy_api(self, remote_url: str, path: str) -> Response:
        """
        Call a proxied API by joining the remote_url to the relative path
        """

        remote_endpoint = join_uri(remote_url, path)

        try:
            if request.method == "GET":
                return requests.get(remote_endpoint).json()
            elif request.method in ["POST", "DELETE", "PUT", "PATCH"]:
                data = request.get_json()
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
                return requests.request(
                    method=request.method,
                    url=remote_endpoint,
                    headers=headers,
                    json=data,
                ).json()
            else:
                raise NotImplementedError(
                    f"Method {request.method} not implemented in the proxy."
                )
        except requests.exceptions.ConnectionError:
            rprint(f"Remote API {remote_url} not available.")
            return Response(status=503)
        except Exception as ex:
            rprint(
                f"An exception occured calling the API {remote_url}. The message is: {ex}"
            )
            return Response(status=500)
