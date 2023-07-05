- [VectorDB Hello World](#vectordb-hello-world)
  - [Pinecone](#pinecone)
  - [OpenSearch](#opensearch)
  - [Vespa](#vespa)
  - [Weaviate](#weaviate)
- [Developing](#developing)
- [License](#license)
- [Copyright](#copyright)

## VectorDB Hello World

Samples of querying vector DBs without using vendor-specific clients.

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
Sign up at [Weaviate Cloud Services WCS](http://console.weaviate.cloud) and create a Weaviate Cluster. You will need your Cluster URL to configure your endpoint https://my_endpoint.weaviate.network. The hello_httpx_test uses httpx library and has examples for addition of one object, batch additions and several queries. 

```
python ./weaviate/hello_httpx_test.py 'https://my_endpoint.weaviate.network' --verbose
```

A running sample for addition of an object

```
Request event hook: GET https://my_endpoint.weaviate.network/v1/objects - Waiting for response
Response event hook: GET https://my_endpoint.weaviate.network/v1/objects - Status 200
https://my_endpoint.weaviate.network/v1/objects
Status code: 200
{
    "deprecations": null,
    "objects": [
        {
            "class": "Athlete",
            "creationTimeUnix": 1688535681981,
            "id": "307262fb-0adc-4c8e-a34e-ca193343c663",
            "lastUpdateTimeUnix": 1688535681981,
            "properties": {
                "age": 26,
                "country": "France",
                "name": "Alldritt",
                "points": 1,
                "rank": 1,
                "sports": "Rugby"
            },
            "vectorWeights": null
        }
    ],
    "totalResults": 1
}
```

Here is an example of batching

```
Request event hook: POST https://my_endpoint.weaviate.network/v1/batch/objects - Waiting for response
Response event hook: POST https://my_endpoint.weaviate.network/v1/batch/objects - Status 200
https://my_endpoint.weaviate.network/v1/batch/objects
Status code: 200
{
......
        {
            "class": "Athlete",
            "creationTimeUnix": 1688535682339,
            "id": "f42e9d7b-8831-4e12-9aa3-bb01554bd2bf",
            "lastUpdateTimeUnix": 1688535682339,
            "properties": {
                "age": 25,
                "country": "USA",
                "name": "Amer1",
                "points": 2890,
                "rank": 5,
                "sports": "Tennis"
            },
            "vectorWeights": null
        }
    ],
    "totalResults": 10
}
```

You can use the hello_httpx_clean.py to delete all objects in your cluster.

```
python ./weaviate/hello_httpx_clean.py 'https://myendpointweaviate.network' --verbose

https://myendpoint.weaviate.network/v1/schema/Athlete
Request event hook: DELETE https://myendpoint.weaviate.network/v1/schema/Athlete - Waiting for response
Response event hook: DELETE https://myendpoint.weaviate.network/v1/schema/Athlete - Status 200
https://myendpoint.network/v1/schema/Athlete
Status code: 200
Request event hook: GET https://myendpoint.weaviate.network/v1/schema - Waiting for response
Response event hook: GET https://myendpoint.weaviate.network/v1/schema - Status 200
https://myendpoint.weaviate.network/v1/schema
Status code: 200
{
    "classes": []
}
```

## Developing

See [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md).

## License

This project is licensed under the [Apache v2.0 License](LICENSE.txt).

## Copyright

Copyright Daniel Doubrovkine, and contributors.
