### Qdrant

Sign up at [Qdrant Cloud Services WCS](http://cloud.qdrant.io/), and create a new free tier Qdrant Cluster with authentication. Note your cluster URL and API key.

```
API_KEY=... ENDPOINT=https://my-cluster.cloud.qdrant.io:6333 poetry run src/qdrant/hello.py

> GET https://my-cluster.cloud.qdrant.io:6333/collections
< GET https://my-cluster.cloud.qdrant.io:6333/collections - 200
> PUT https://my-cluster.cloud.qdrant.io:6333/collections/my-index
< PUT https://my-cluster.cloud.qdrant.io:6333/collections/my-index - 200
> PUT https://my-cluster.cloud.qdrant.io:6333/collections/my-index/points?wait=true
< PUT https://my-cluster.cloud.qdrant.io:6333/collections/my-index/points?wait=true - 200
> POST https://my-cluster.cloud.qdrant.io:6333/collections/my-index/points/search
< POST https://my-cluster.cloud.qdrant.io:6333/collections/my-index/points/search - 200
{'result': [{'id': 1, 'version': 0, 'score': 0.9999998, 'payload': None, 'vector': None}], 'status': 'ok', 'time': 0.000117235}
> DELETE https://my-cluster.cloud.qdrant.io:6333/collections/my-index
< DELETE https://my-cluster.cloud.qdrant.io:6333/collections/my-index - 200
```
