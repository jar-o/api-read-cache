"""
    General configuration for the 'common' package.
"""
import os
class Config:
    # This is the central cache server, that keeps the 'root' or raw cached
    # responses from the Github API (not any derived ones in /views'

    MASTER_CACHE_HOST = 'localhost'
    MASTER_CACHE_PORT = 6379
    MASTER_CACHE_PASSWORD = os.environ.get('CACHE_PASSWORD')
    MASTER_CACHE_TTL = 1000 # seconds

    GITHUB_API_PREFIX = 'https://api.github.com'
    GITHUB_API_TOKEN = os.environ.get('GITHUB_API_TOKEN')

    # Each node caches responses too. Can be overridden at the view level.
    NODE_CACHE_CONFIG = {
        'CACHE_TYPE': 'simple',
        'CACHE_DEFAULT_TIMEOUT': 50 # seconds
    }
