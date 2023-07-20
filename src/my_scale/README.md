### MyScale

[MyScale](https://myscale.com) performs vector search in SQL, and [claims](https://blog.myscale.com/2023/05/17/myscale-outperform-special-vectordb/) to outperform other solutions by using a proprietary algorithm called MSTG. MyScale is built on the open-source ClickHouse (see [this sample](../click_house/README.md)). 

Sign up [on their website](https://myscale.com) for a test cluster, note the username and password, then run the working sample as follows.

```
poetry install
USERNAME=... PASSWORD=... ENDPOINT=https://...aws.myscale.com:443 poetry run ./hello.py

> POST https://...aws.myscale.com
  CREATE TABLE IF NOT EXISTS default.vectors (id String,values Array(Float32),CONSTRAINT check_length CHECK length(values) = 3,VECTOR INDEX values_index values TYPE MSTG) ENGINE = MergeTree ORDER BY id
< POST https://...aws.myscale.com - 200
> POST https://...aws.myscale.com
  INSERT INTO default.vectors (id, values) VALUES ('vec1', [0.1, 0.2, 0.3])
< POST https://...aws.myscale.com - 200
> POST https://...aws.myscale.com
  INSERT INTO default.vectors (id, values) VALUES ('vec2', [0.2, 0.3, 0.4])
< POST https://...aws.myscale.com - 200
> POST https://...aws.myscale.com
  SELECT * FROM default.vectors ORDER BY L2Distance(values, [0.2, 0.3, 0.4])
< POST https://...aws.myscale.com - 200
vec2	[0.2,0.3,0.4]
vec1	[0.1,0.2,0.3]

> POST https://...aws.myscale.com
  DROP TABLE default.vectors
< POST https://...aws.myscale.com - 200
```
