import json
import os
import sys

import pytest

from flask_reactize import FlaskReactize


@pytest.fixture()
def sample_data_folder():
    return os.path.join(os.path.dirname(__file__), "sample_data")


@pytest.fixture()
def send_from_directory_patch(monkeypatch: pytest.MonkeyPatch):
    def mock_send_from_directory(directory, path):
        return path

    monkeypatch.setattr(
        sys.modules["flask_reactize.flask_reactize"],
        "send_from_directory",
        lambda directory, path: mock_send_from_directory(directory, path),
    )


def test_FlaskReactize_init_none():
    with pytest.raises(ValueError):
        flask_reactize = FlaskReactize(None)
        assert flask_reactize is not None


def test_FlaskReactize_init_ok(flask_app):
    flask_reactize = FlaskReactize(flask_app)
    assert flask_reactize is not None


def test_FlaskReactize_serve_static_param_static_folder_none(flask_app):
    with pytest.raises(ValueError):
        FlaskReactize(flask_app).serve_static(None)


def test_FlaskReactize_serve_static_param_static_folder_invalid(flask_app):
    with pytest.raises(ValueError):
        FlaskReactize(flask_app).serve_static("some_folder")


def test_FlaskReactize_serve_static_param_static_folder_ok(
    flask_app, sample_data_folder
):
    FlaskReactize(flask_app).serve_static(sample_data_folder)

    assert (
        len(list(flask_app.url_map.iter_rules())) == 3
        and len(list(flask_app.url_map.iter_rules("static"))) == 1
    )


@pytest.mark.parametrize(
    "path,content", [("", "index.html"), ("some_file.txt", "some_file.txt")]
)
def test_FlaskReactize__send_static_with_path(
    flask_app, sample_data_folder, send_from_directory_patch, path, content
):
    assert (
        FlaskReactize(flask_app)._FlaskReactize__send_static(sample_data_folder, path)
        == content
    )


def test_serve_react_app_param_source_none(flask_app):
    with pytest.raises(ValueError):
        FlaskReactize(flask_app).serve_react_app(None)


def test_serve_react_app_param_source_invalid(flask_app):
    with pytest.raises(ValueError):
        FlaskReactize(flask_app).serve_react_app("some_folder")


def test_serve_react_app_param_source_ok(flask_app, sample_data_folder):
    FlaskReactize(flask_app).serve_react_app(sample_data_folder)

    assert (
        len(list(flask_app.url_map.iter_rules())) == 2
        and len(list(flask_app.url_map.iter_rules("static"))) == 0
    )


def test_serve_react_app_check_reactjs_default_port(flask_app, sample_data_folder):
    FlaskReactize(flask_app).serve_react_app(sample_data_folder)

    assert os.environ["WDS_SOCKET_PORT"] == "3005"


def test_serve_react_app_check_reactjs_custom_port(flask_app, sample_data_folder):
    FlaskReactize(flask_app).serve_react_app(sample_data_folder, port=3000)

    assert os.environ["WDS_SOCKET_PORT"] == "3000"


def test__route_react_http_no_header(requests_mock, flask_app):
    requests_mock.register_uri(
        "GET",
        "http://127.0.0.1:3005/some_path",
        content=b"some content",
        status_code=200,
    )

    with pytest.raises(Exception):
        FlaskReactize(flask_app)._FlaskReactize__route_react_http(
            3005, "some_path"
        ).get_data() == b"some content"


def test__route_react_http_invalid_path(requests_mock, flask_app):
    requests_mock.register_uri(
        "GET",
        "http://127.0.0.1:3005/some_path_fake",
        content=b"some content",
        headers={"Content-Type": "text/html"},
        status_code=200,
    )

    with pytest.raises(Exception):
        FlaskReactize(flask_app)._FlaskReactize__route_react_http(
            3005, "some_path"
        ).get_data() == b"some content"


def test__route_react_http_ok(requests_mock, flask_app):
    requests_mock.register_uri(
        "GET",
        "http://127.0.0.1:3005/some_path",
        content=b"some content",
        headers={"Content-Type": "text/html"},
        status_code=200,
    )

    assert (
        FlaskReactize(flask_app)
        ._FlaskReactize__route_react_http(3005, "some_path")
        .get_data()
        == b"some content"
    )


def test__set_proxy_api(flask_app):
    proxy_api = {
        "/route1": "http://some_url/api",
        "/route2": "http://some_other_url/api/v1",
    }

    FlaskReactize(flask_app)._FlaskReactize__set_proxy_api(proxy_api)

    assert (
        len(list(flask_app.url_map.iter_rules("/route1/<path:path>"))) == 1
        and len(list(flask_app.url_map.iter_rules("/route2/<path:path>"))) == 1
    )


@pytest.mark.parametrize("method", ["GET", "POST", "PATCH", "DELETE", "PUT"])
def test__serve_proxy_api(requests_mock, flask_app, method):
    x = {"name": "John", "job": "TPM"}

    requests_mock.register_uri(
        method,
        "http://some_uri/api/users",
        json=json.dumps(x),
        headers={"Content-Type": "application/json"},
        status_code=200,
    )

    with flask_app.test_request_context(method=method):
        resp = FlaskReactize(flask_app)._FlaskReactize__serve_proxy_api(
            "http://some_uri", "api/users"
        )

        assert json.loads(resp)["name"] == "John"


def test__serve_proxy_api_method_not_implemented(requests_mock, flask_app):
    x = {"name": "John", "job": "TPM"}

    requests_mock.register_uri(
        "OPTIONS",
        "http://some_uri/api/users",
        json=json.dumps(x),
        headers={"Content-Type": "application/json"},
        status_code=200,
    )

    with flask_app.test_request_context(method="OPTIONS"):
        resp = FlaskReactize(flask_app)._FlaskReactize__serve_proxy_api(
            "http://some_uri", "api/users"
        )

        assert resp.status_code == 500
