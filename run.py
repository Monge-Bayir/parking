from flask import Flask

from app import create_app
from config import Config

app: Flask = create_app(config_class=Config)

if __name__ == "__main__":
    app.run()
