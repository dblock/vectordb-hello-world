### OpenSearch

You can use a managed service (e.g. [Amazon OpenSearch](https://aws.amazon.com/opensearch-service/)), or download and run open-source OpenSearch with Docker.

```
docker pull opensearchproject/opensearch:latest
docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

Run a working sample as follows.

```
poetry install
USERNAME=admin PASSWORD=admin ENDPOINT=https://localhost:9200 poetry run ./hello.py

> GET https://localhost:9200/_cat/indices
< GET https://localhost:9200/_cat/indices - 200
> PUT https://localhost:9200/my-index
< PUT https://localhost:9200/my-index - 200
> POST https://localhost:9200/_bulk
< POST https://localhost:9200/_bulk - 200
> POST https://localhost:9200/my-index/_search
< POST https://localhost:9200/my-index/_search - 200
{'total': {'value': 1, 'relation': 'eq'}, 'max_score': 0.97087383, 'hits': [{'_index': 'my-index', '_id': 'vec1', '_score': 0.97087383, '_source': {'index': {'_index': 'my-index', '_id': 'vec2'}, 'vector': [0.2, 0.3, 0.4], 'metadata': {'genre': 'action'}}}]}
> DELETE https://localhost:9200/my-index
< DELETE https://localhost:9200/my-index - 200
```

See also [this example](hello-with-filter.py) that creates an index using a different k-nn engine and filters data by genre.