### Weaviate

Sign up at [Weaviate Cloud Services WCS](http://console.weaviate.cloud), and create a new free tier Weaviate Cluster with authentication. Note your cluster URL and API key.

```
API_KEY=... ENDPOINT=https://my-cluster.weaviate.network poetry run src/weaviate/hello.py


> POST https://myindex.weaviate.network/v1/batch/objects
< POST https://myindex.weaviate.network/v1/batch/objects - 200
> GET https://myindex.weaviate.network/v1/objects?fields=vector&nearVector=%7B%27vector%27%3A%20%5B0.1%5D%2C%20%27certainty%27%3A%200.9%7D
< GET https://myindex.weaviate.network/v1/objects?fields=vector&nearVector=%7B%27vector%27%3A%20%5B0.1%5D%2C%20%27certainty%27%3A%200.9%7D - 200
{'class': 'Vectors', 'creationTimeUnix': 1688914857307, 'id': '46e40d05-d550-4415-aa2c-7c004fcdd037', 'lastUpdateTimeUnix': 1688914857307, 'properties': {'vector': [0.1, 0.2, 0.3]}, 'vectorWeights': None}
{'class': 'Vectors', 'creationTimeUnix': 1688914857307, 'id': 'c14bd5b1-8b81-44a4-8051-3b9b8c52cde4', 'lastUpdateTimeUnix': 1688914857307, 'properties': {'vector': [0.2, 0.3, 0.4]}, 'vectorWeights': None}
> DELETE https://myindex.weaviate.network/v1/schema/Vectors
< DELETE https://myindex.weaviate.network/v1/schema/Vectors - 200
```
