from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app, db
from config import TestConfig


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
