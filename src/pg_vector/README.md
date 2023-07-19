### pgVector

[pgVector](https://github.com/pgvector/pgvector) adds vector similarity search to Postgres. You can use a local docker installation from [ankane/pgvector](https://hub.docker.com/r/ankane/pgvector) or a [managed service](https://github.com/pgvector/pgvector#hosted-postgres). 

```
docker pull ankane/pgvector or https://github.com/pgvector/pgvector/issues/54 for cloud providers
docker run -e POSTGRES_PASSWORD=password -p 5433:5432 ankane/pgvector
```

PostgreSQL does not speak HTTP like the other databases, so we need some dependencies. Run a working sample as follows.

```
poetry install
PGPORT=5433 PGUSER=postgres PGPASSWORD=password poetry run ./hello.py

<Record id='vec2' values=array([0.2, 0.3, 0.4], dtype=float32) metadata='{"genre": "action"}'> (action)
```
