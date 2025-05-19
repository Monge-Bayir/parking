from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import Type

from config import Config

db = SQLAlchemy()

def create_app(config_class: Type[Config]) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from .routers import bp
    app.register_blueprint(bp)

    return app