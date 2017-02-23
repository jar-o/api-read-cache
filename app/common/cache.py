from flask_cache import Cache
from config import Config
cache = Cache(config=Config.NODE_CACHE_CONFIG)
