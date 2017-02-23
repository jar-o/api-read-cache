import time, requests, json
from config import Config # See common/config.py
import redis
from redlock import RedLock

cachesrv = redis.StrictRedis(
    host=Config.MASTER_CACHE_HOST,
    port=Config.MASTER_CACHE_PORT,
    db=0)

def master_cache(func):
    def wrapper(*args):
        conn = [{'host': Config.MASTER_CACHE_HOST, 'port': Config.MASTER_CACHE_PORT, 'db': 0}]
        k = str(args[0].__class__) + func.__name__
        v = cachesrv.get(k)
        if not v:
            with RedLock(k + '.lock', connection_details=conn):
                v = json.dumps(func(*args))
                cachesrv.set(k, v, Config.MASTER_CACHE_TTL)
        return v
    return wrapper

class GithubGrab(object):
    def __init__(self):
        self.gh_prefix = Config.GITHUB_API_PREFIX
        self.headers = {}
        if Config.GITHUB_API_TOKEN:
            self.headers['Authorization'] = 'token ' + Config.GITHUB_API_TOKEN

    @master_cache
    def get_any(self, reqpath):
        return json.dumps(self.__get_all(self.__get(self.gh_prefix + reqpath)))

    def __get(self, url = ''):
        if url.startswith('/'):
            return requests.get(self.gh_prefix + url)
        else:
            return requests.get(url)

    def __get_all(self, req):
        data = json.loads(req.content)
        if type(data) is not list:
            return data
        while req.links and 'next' in req.links:
            data += json.loads(req.content)
            req = self.__get(req.links['next']['url'])
        return data

    @master_cache
    def netflix_orgs(self):
        return json.loads(self.__get('/orgs/Netflix').content)

    @master_cache
    def github_root(self):
        return json.loads(self.__get(self.gh_prefix).content)

    @master_cache
    def all_netflix_repos(self):
        return self.__get_all(self.__get('/orgs/Netflix/repos'))

    @master_cache
    def all_netflix_members(self):
        return self.__get_all(self.__get('/orgs/Netflix/members'))
