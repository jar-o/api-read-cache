"""
 The view endpoints.
"""
import json, datetime
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify, make_response)
from app.common import GithubGrab, cache

view = Blueprint('view', 'view', url_prefix='/view')
grab = GithubGrab()

# Used by most of the views below
def topn(num, count_key):
    prep = {}
    for el in json.loads(grab.all_netflix_repos()):
        prep[el[count_key]] = el

    data = []
    for k in sorted(prep.keys(), reverse=True):
        data.append([ prep[k]['full_name'], prep[k][count_key] ])
    return jsonify(data[:int(num)])

@view.route('/top/<num>/forks', methods=['GET'])
@cache.memoize()
def top_forks(num):
    return topn(num, 'forks_count')

@view.route('/top/<num>/open_issues', methods=['GET'])
@cache.memoize()
def top_open_issues(num):
    return topn(num, 'open_issues')

@view.route('/top/<num>/stars', methods=['GET'])
@cache.memoize()
def top_stars(num):
    return topn(num, 'stargazers_count')

@view.route('/top/<num>/watchers', methods=['GET'])
@cache.memoize()
def top_watchers(num):
    return topn(num, 'watchers_count')

@view.route('/top/<num>/last_updated', methods=['GET'])
@cache.memoize()
def top_last_updated(num):
    prep = {}
    for el in json.loads(grab.all_netflix_repos()):
        prep[iso8601_to_epoch(el['updated_at'])] = el

    data = []
    for k in sorted(prep.keys(), reverse=True):
        data.append([ prep[k]['full_name'], prep[k]['updated_at'] ])
    return jsonify(data[:int(num)])

def iso8601_to_epoch(s):
    d = datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ" )
    return int(d.strftime("%s")) * 1000
