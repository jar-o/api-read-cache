"""
 The root API endpoints.
"""
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)
from app.common import GithubGrab, cache

root = Blueprint('root', __name__)
grab = GithubGrab()

@root.route('/healthcheck', methods=['GET'])
def healthcheck():
    return ('', 200)

@root.route('/', methods=['GET'])
@cache.cached() # NOTE(james) must come right before method
def index():
    return grab.github_root()

@root.route('/orgs/Netflix', methods=['GET'])
@cache.cached()
def netflix_orgs():
    return grab.netflix_orgs()

@root.route('/orgs/Netflix/repos', methods=['GET'])
@cache.cached()
def netflix_repos():
    return grab.all_netflix_repos()

@root.route('/orgs/Netflix/members', methods=['GET'])
@cache.cached()
def netflix_members():
    return grab.all_netflix_members()

## NOTE(james) Requests that land here are only cached by the individual nodes
## running this app, not the master cache
@root.route('/<path:dummy>')
def fallback(dummy):
   return jsonify(grab.get_any(request.path))
