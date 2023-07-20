### ClickHouse

[ClickHouse](https://clickhouse.com/) is a fast and resource efficient open-source database for real-time apps and analytics. You can [download a free version](https://clickhouse.com/#getting_started) or use [ClickHouse Cloud](https://clickhouse.com/).

```
docker run -p 9000:9000 -p 9009:9009 -p 8123:8123 --platform linux/amd64 --ulimit nofile=262144:262144 clickhouse/clickhouse-server
```

Run a working sample as follows.

```
poetry install
poetry run ./hello.py

> POST http://localhost:8123?allow_experimental_annoy_index=1
  CREATE TABLE IF NOT EXISTS default.vectors (id String,values Array(Float32),CONSTRAINT check_length CHECK length(values) = 3,INDEX values_index values TYPE annoy GRANULARITY 100) ENGINE = MergeTree ORDER BY id
< POST http://localhost:8123?allow_experimental_annoy_index=1 - 200
> POST http://localhost:8123
  INSERT INTO default.vectors (id, values) VALUES ('vec1', [0.1, 0.2, 0.3])
< POST http://localhost:8123 - 200
> POST http://localhost:8123
  INSERT INTO default.vectors (id, values) VALUES ('vec2', [0.2, 0.3, 0.4])
< POST http://localhost:8123 - 200
> POST http://localhost:8123
  SELECT * FROM default.vectors ORDER BY L2Distance(values, [0.2, 0.3, 0.4])
< POST http://localhost:8123 - 200
vec2	[0.2,0.3,0.4]
vec1	[0.1,0.2,0.3]

> POST http://localhost:8123
  DROP TABLE default.vectors
< POST http://localhost:8123 - 200
```
