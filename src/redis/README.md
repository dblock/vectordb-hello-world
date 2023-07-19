### Redis

You can use a managed service (e.g. [Redis.com](https://redis.com/)), or download and run open-source Redis with Docker.

```
docker run -p 6379:6379 redislabs/redisearch:latest
```

Redis does not speak HTTP like the other databases, so we need some dependencies. Run a working sample as follows.

```
poetry install
poetry run ./hello.py

Document {'id': 'doc:2', 'payload': None, 'score': '0.00741678476334', 'genre': 'action'}
```

See [redis-py#2854](https://github.com/redis/redis-py/issues/2854) for a question on enabling Redis logging like in other samples.
