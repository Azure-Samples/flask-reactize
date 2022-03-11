from urllib.parse import urljoin

from flask import Flask


class bcolors:
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    DEFAULT = "\033[0m"


def rprint(input: str) -> None:
    """
    Prints reactjs output with color in order to stand in the console
    """

    print(f"{bcolors.GREEN}[REACT] {input} {bcolors.DEFAULT}")


def clear_flask_default_status_rule(
    flask_app: Flask, add_default_route: bool = True
) -> None:
    """
    Flask define a default 'static' route that interfere with react app files.
    This utility method, called internally resets it
    """

    for rule in flask_app.url_map.iter_rules("static"):
        flask_app.url_map._rules.remove(rule)
        flask_app.view_functions["static"] = None

    flask_app.url_map._rules_by_endpoint["static"] = []

    if add_default_route:
        flask_app.add_url_rule(
            "/<path:filename>", endpoint="static", view_func=flask_app.send_static_file
        )


def join_uri(url1, url2):
    return urljoin(url1, url2) if url1.endswith("/") else urljoin(f"{url1}/", url2)
