import pytest
from flask import Flask


@pytest.fixture
def flask_app() -> Flask:
    return Flask(__name__)
