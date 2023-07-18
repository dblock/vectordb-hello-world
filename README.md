- [VectorDB Hello World](#vectordb-hello-world)
  - [Pinecone](#pinecone)
  - [OpenSearch](#opensearch)
  - [Vespa](#vespa)
  - [Weaviate](#weaviate)
  - [Qdrant](#qdrant)
  - [Redis](#redis)
- [Developing](#developing)
- [License](#license)
- [Copyright](#copyright)

## VectorDB Hello World

Samples of querying vector DBs without using vendor-specific clients. See [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md) if you need to get setup with Python and poetry.

### Pinecone

Sign up for [Pinecone](https://pinecone.io), get an `API_TOKEN` and a `PROJECT_ID`.

Run a working sample as follows.

```
API_KEY=... PROJECT_ID=... ENDPOINT=https://us-west4-gcp-free.pinecone.io poetry run src/pinecone/hello.py

> GET https://controller.us-west4-gcp-free.pinecone.io/databases
< GET https://controller.us-west4-gcp-free.pinecone.io/databases - 200
> POST https://my-index-c7556fa.svc.us-west4-gcp-free.pinecone.io/vectors/upsert
< POST https://my-index-c7556fa.svc.us-west4-gcp-free.pinecone.io/vectors/upsert - 200
> POST https://my-index-c7556fa.svc.us-west4-gcp-free.pinecone.io/query
< POST https://my-index-c7556fa.svc.us-west4-gcp-free.pinecone.io/query - 200
{'results': [], 'matches': [{'id': 'vec1', 'score': 0.999999881, 'values': [], 'metadata': {'genre': 'drama'}}], 'namespace': 'namespace'}
```

### OpenSearch

You can use a managed service (e.g. [Amazon OpenSearch](https://aws.amazon.com/opensearch-service/)), or download and run open-source OpenSearch with Docker.

```
docker pull opensearchproject/opensearch:latest
docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

Run a working sample as follows.

```
USERNAME=admin PASSWORD=admin ENDPOINT=https://localhost:9200 poetry run src/open_search/hello.py

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

### Vespa

You can use the [vespa.ai cloud service](https://cloud.vespa.ai/), or download and run [Vespa](https://vespa.ai/) with Docker.

Make sure you [configure Docker with at least 4GB RAM](https://docs.docker.com/desktop/settings/mac/#resources).

```sh
docker info | grep "Total Memory" # make sure it's at least 4Gb
docker pull vespaengine/vespa
```

Start Vespa.

```
docker run --detach --name vespa --hostname vespa-container \
  --publish 8080:8080 --publish 19071:19071 \
  vespaengine/vespa
```

Deploy the sample application and schema.

```sh
(cd src/vespa/vector-app && zip -r - .) | \
  curl --header Content-Type:application/zip --data-binary @- \
  localhost:19071/application/v2/tenant/default/prepareandactivate

curl --header Content-Type:application/zip -XPOST localhost:19071/application/v2/tenant/default/session
```

Finally, run the Vespa sample ingestion and search. You might have to wait for a few seconds for the endpoint to be ready after the last command.

```sh
ENDPOINT=http://localhost:8080 CONFIG_ENDPOINT=http://localhost:19071 poetry run src/vespa/hello.py

> POST http://localhost:8080/document/v1/vector/vector/docid/vec1
< POST http://localhost:8080/document/v1/vector/vector/docid/vec1 - 200
> POST http://localhost:8080/document/v1/vector/vector/docid/vec2
< POST http://localhost:8080/document/v1/vector/vector/docid/vec2 - 200
> GET http://localhost:8080/search/?yql=select%20%2A%20from%20sources%20%2A%20where%20%7BtargetHits%3A%201%7D%20nearestNeighbor%28values%2Cvector_query_embedding%29&ranking.profile=vector_similarity&hits=1&input.query%28vector_query_embedding%29=%5B0.1%2C0.2%2C0.3%5D
< GET http://localhost:8080/search/?yql=select%20%2A%20from%20sources%20%2A%20where%20%7BtargetHits%3A%201%7D%20nearestNeighbor%28values%2Cvector_query_embedding%29&ranking.profile=vector_similarity&hits=1&input.query%28vector_query_embedding%29=%5B0.1%2C0.2%2C0.3%5D - 200
{'sddocname': 'vector', 'documentid': 'id:vector:vector::vec1', 'id': 'vec1', 'values': {'type': 'tensor<float>(x[3])', 'values': [0.10000000149011612, 0.20000000298023224, 0.30000001192092896]}, 'metadata': {'genre': 'drama'}}
> DELETE http://localhost:19071/application/v2/tenant/default/application/default
< DELETE http://localhost:19071/application/v2/tenant/default/application/default - 200
```

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

### Redis

You can use a managed service (e.g. [Redis.com](https://redis.com/)), or download and run open-source Redis with Docker.

```
docker run -p 6379:6379 redislabs/redisearch:latest
```

Redis does not speak HTTP like the other databases, so we need some dependencies. Run a working sample as follows.

```
cd src/redis
poetry install
poetry run ./hello.py

Document {'id': 'doc:2', 'payload': None, 'score': '0.00741678476334', 'genre': 'action'}
```

See [redis-py#2854](https://github.com/redis/redis-py/issues/2854) for a question on enabling Redis logging like in other samples.

## Developing

See [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md).

## License

This project is licensed under the [Apache v2.0 License](LICENSE.txt).

## Copyright

Copyright Daniel Doubrovkine, and contributors.
