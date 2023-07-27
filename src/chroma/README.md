### Chroma

[Chroma](https://www.trychroma.com/) is an AI-native open-source embedding database.

Clone Chroma from GitHub and run it locally.

```
git clone https://github.com/chroma-core/chroma.git
cd chroma
docker-compose up -d --build
```

Check Chroma version with `curl http://localhost:8000/api/v1/version`.

Run the sample.

```
poetry install
ENDPOINT=http://localhost:8000 poetry run ./hello.py

$ ENDPOINT=http://localhost:8000 poetry run ./hello.py
> GET http://localhost:8000/api/v1/version
< GET http://localhost:8000/api/v1/version - 200
Chroma 0.4.3
> GET http://localhost:8000/api/v1/collections
< GET http://localhost:8000/api/v1/collections - 200
> POST http://localhost:8000/api/v1/collections
< POST http://localhost:8000/api/v1/collections - 200
> POST http://localhost:8000/api/v1/collections/f5aae9cc-a0c1-4990-9942-7a47542b9f64/add
< POST http://localhost:8000/api/v1/collections/f5aae9cc-a0c1-4990-9942-7a47542b9f64/add - 201
> POST http://localhost:8000/api/v1/collections/f5aae9cc-a0c1-4990-9942-7a47542b9f64/query
< POST http://localhost:8000/api/v1/collections/f5aae9cc-a0c1-4990-9942-7a47542b9f64/query - 200
{'ids': [['c47eade8-59b9-4c49-9172-a0ce3d9dd0af']], 'distances': None, 'metadatas': [[{'genre': 'action'}]], 'embeddings': [[[0.2, 0.3, 0.4]]], 'documents': None}
> DELETE http://localhost:8000/api/v1/collections/my-collection
< DELETE http://localhost:8000/api/v1/collections/my-collection - 200
```
