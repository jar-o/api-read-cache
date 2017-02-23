import os
from flask import Response
from common.constants import INSTANCE_FOLDER_PATH

# defaults to JSON mime type on all views
class AppResponse(Response):
    default_mimetype = 'application/json'

class BaseConfig(object):

   PROJECT = "app"

   # Get app root path, also can use flask.root_path.
   PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

   DEBUG = False
   TESTING = False

   ADMINS = ['traptoy@gmail.com']

   APP_RESPONSE = AppResponse

class DefaultConfig(BaseConfig):
    DEBUG = True

class LocalConfig(DefaultConfig):
    pass

class ProdConfig(DefaultConfig):
    pass

def get_config(MODE):
    SWITCH = {
        'LOCAL'     : LocalConfig,
        'PRODUCTION': ProdConfig
    }
    return SWITCH[MODE]
