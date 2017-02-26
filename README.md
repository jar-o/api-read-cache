# API Read Cache

## Overview

This is a Flask/Python API app that acts as a content cache for the Github API. It is designed with two levels of cache.

The primary (or "master") cache stores the expanded content of the following Github API endpoints:

```
/
/orgs/Netflix
/orgs/Netflix/members
/orgs/Netflix/repos
```

In this implementation the master cache is facilitated by a Redis server.

Each API node that runs this Flask app acts as a *secondary* cache. The endpoints that are accessed will store the results generated locally, and serve that until it expires. Typically the expiration on the local API node caches are shorter than the master cache, but that is configurable.

The basic configuration would look like:

* A single Redis cache server
* 1 or more API nodes

When the master cache content expires we use a [Redlock](https://redis.io/topics/distlock) to restrict updating the primary cache to a single node so that the Github API is never overwhelmed even if there are multiple API nodes in operation.

## Setup

**Prerequisites**: Python/pip, Redis

To get started, clone this repository, then `cd` into the folder and do

```
pip install -r requirements.txt
```

To run the server you can invoke it like

```
GITHUB_API_TOKEN=... python run.py 7101
```

Note that `GITHUB_API_TOKEN` is optional, but you'll hit an API limit if you don't use it.

Also, `run.py` takes a single optional parameter, that of the PORT number. If you omit this, it will default to `5000`.

Additionally, your Redis server may require a password. In that case you can set the `CACHE_PASSWORD` environment variable.

### Configuration

There are two primary configuration files. The Flask config file under `app/config.py` and the config for the business logic modules under `app/common/config.py`.

### Testing

You can test with the originally provided `api_test_suite.sh`. However, to get to at least 68% passing, I had to make some edits. See `test_suite.patch`. You should be able to do

```
patch api_test_suite.sh < test_suite.patch
```

then run `api_test_suite.sh` to verify.

## Unfinished business

* There are no Flask unit tests or otherwise
* Exception handling needs to be added, at least for the basic cases of servers not responding, etc

