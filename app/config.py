import os
from flask import Response
from common.constants import INSTANCE_FOLDER_PATH

# defaults to JSON mime type on all views. Simply modify the mime type below if
# you ever switch to say... xml?
class AppResponse(Response):
    default_mimetype = 'application/json'

class BaseConfig(object):

   PROJECT = "app"

   PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

   DEBUG = False
   TESTING = False

   ADMINS = ['admin@example.com']

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
