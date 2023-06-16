- [VectorDB Hello World](#vectordb-hello-world)
  - [Pinecone](#pinecone)
  - [OpenSearch](#opensearch)
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
```

### OpenSearch

You can use a managed service (e.g. [Amazon OpenSearch](https://aws.amazon.com/opensearch-service/)), or download and run open-source OpenSearch.

```
docker pull opensearchproject/opensearch:latest
docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest
```

Run a working sample as follows.

```
USERNAME=admin PASSWORD=admin ENDPOINT=https://localhost:9200 poetry run src/open_search/hello.py
```

## Developing

See [DEVELOPER_GUIDE](DEVELOPER_GUIDE.md).

## License

This project is licensed under the [Apache v2.0 License](LICENSE.txt).

## Copyright

Copyright Daniel Doubrovkine, and contributors.
