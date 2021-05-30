from flask import Flask

from config import config_options


def create_app(config: str):
    app = Flask(__name__)

    app.config.from_object(config_options.get(config, 'production'))

    from .parking_detector import parking as parking_blueprint
    app.register_blueprint(parking_blueprint, url_prefix='')

    return app
