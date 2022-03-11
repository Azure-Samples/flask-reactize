from flask_reactize.utils import clear_flask_default_status_rule, join_uri


def test_clear_flask_default_status_rule_with_default_route(flask_app):
    clear_flask_default_status_rule(flask_app)

    assert len(list(flask_app.url_map.iter_rules("static"))) == 1


def test_clear_flask_default_status_rule_no_default_route(flask_app):
    clear_flask_default_status_rule(flask_app, False)

    assert len(list(flask_app.url_map.iter_rules("static"))) == 0


def test_join_uri_no_slash():
    prefix = "http://localhost"
    suffix = "api/users"

    url = join_uri(prefix, suffix)

    assert url == "http://localhost/api/users"


def test_join_uri():
    prefix = "http://localhost/"
    suffix = "api/users"

    url = join_uri(prefix, suffix)

    assert url == "http://localhost/api/users"
