#!/usr/bin/env python

import os
from urllib.parse import urljoin

from httpx import Client, Response


def log_request(request):
    print(f"> {request.method} {request.url}")


def log_response(response):
    request = response.request
    print(f"< {request.method} {request.url} - {response.status_code}")
    if response.status_code >= 299:
        response.read()
        print(f"\n{response.text}")


def main():
    # HTTP setup
    endpoint = os.getenv("ENDPOINT", 'http://localhost:8000')
    api_url = urljoin(endpoint, '/api/v1/')
    client = Client(
        event_hooks={
            "request": [log_request],
            "response": [log_response, Response.raise_for_status],
        },
    )
    headers = {
        "Accept": "application/json; charset=utf-8",
        "Content-Type": "application/json; charset=utf-8",
    }

    version = client.get(urljoin(api_url, 'version'), headers=headers).json()
    print(f"Chroma {version}")

    # check whether a collection exists
    collection_name = "my-collection"
    collections = client.get(urljoin(api_url, "collections"), headers=headers).json()
    collection = next((x for x in collections if x["name"] == collection_name), None)
    if not collection:
        collection = client.post(
            urljoin(api_url, "collections"),
            headers=headers,
            json={
                "name": collection_name
            },
        ).json()

    # index data
    vectors = [
        {
            "id": "d8f940f1-d6c1-4d8e-82c1-488eb7801e57",
            "values": [0.1, 0.2, 0.3],
            "metadata": {"genre": "drama"},
        },
        {
            "id": "c47eade8-59b9-4c49-9172-a0ce3d9dd0af",
            "values": [0.2, 0.3, 0.4],
            "metadata": {"genre": "action"},
        },
    ]

    # prepare data
    data = {
        "ids": [],
        "embeddings": [],
        "metadatas": []
    }

    for vector in vectors:
        data["ids"].append(vector["id"])
        data["embeddings"].append(vector["values"])
        data["metadatas"].append(vector["metadata"])

    client.post(urljoin(api_url, f"collections/{collection['id']}/add"), headers=headers, json=data)

    # search
    query = {
        "query_embeddings": [[0.15, 0.12, 1.23]], 
        "n_results": 1,
        "include":["embeddings", "metadatas"]
    }

    results = client.post(
        urljoin(api_url, f"collections/{collection['id']}/query"), headers=headers, json=query
    ).json()

    print(results)

    # delete collection
    client.delete(urljoin(api_url, f"collections/{collection_name}"), headers=headers)

if __name__ == "__main__":
    main()
