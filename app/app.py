import os
from flask import Flask
import config as Config
from .common import constants as COMMON_CONSTANTS, cache
from .api import root, view

__all__ = ['create_app'] # For import *

DEFAULT_BLUEPRINTS = [ root, view ]

def create_app(config=None, app_name=None, blueprints=None):

    if app_name is None:
        app_name = Config.DefaultConfig.PROJECT

    app = Flask(
        app_name,
        instance_path=COMMON_CONSTANTS.INSTANCE_FOLDER_PATH,
        instance_relative_config=True
    )
    configure_app(app, config)
    cache.init_app(app)

    configure_blueprints(app, DEFAULT_BLUEPRINTS)
    configure_error_handlers(app)
    return app

def configure_app(app, config=None):
    # Get app mode from environment, default to local
    application_mode = os.getenv('APPLICATION_MODE', 'LOCAL')
    app.config.from_object(Config.get_config(application_mode))

    # Set the response type on all views (to JSON)
    app.response_class = app.config['APP_RESPONSE']

def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

# TODO james
def configure_error_handlers(app):
    # example
    @app.errorhandler(500)
    def server_error_page(error):
        return "ERROR PAGE!"
