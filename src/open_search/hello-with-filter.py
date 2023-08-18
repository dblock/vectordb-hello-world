#!/usr/bin/env python

import os
import time
import json
from httpx import Client, BasicAuth, Response
from urllib.parse import urljoin


def log_request(request):
    print(f"> {request.method} {request.url}")


def log_response(response):
    request = response.request
    print(f"< {request.method} {request.url} - {response.status_code}")
    if response.status_code >= 299:
        response.read()
        print(f"\n{response.text}")


def main():
    # HTTPs setup
    endpoint = os.environ["ENDPOINT"]
    auth = BasicAuth(username=os.environ["USERNAME"], password=os.environ["PASSWORD"])
    client = Client(
        verify=False,
        auth=auth,
        event_hooks={
            "request": [log_request],
            "response": [log_response, Response.raise_for_status],
        },
    )
    headers = {
        "Accept": "application/json; charset=utf-8",
        "Content-Type": "application/json; charset=utf-8",
    }

    # check whether an index exists
    index_name = "my-index"

    indices = {
        x["index"]: x
        for x in client.get(urljoin(endpoint, "/_cat/indices"), headers=headers).json()
    }
    if not index_name in indices:
        client.put(
            urljoin(endpoint, f"/{index_name}"),
            headers=headers,
            json={
                "settings": {
                    "index.knn": True
                },
                "mappings": {
                    "properties": {
                        "values": {
                            "type": "knn_vector",
                            "dimension": 3,
                            "method": {
                                "name": "hnsw",
                                "space_type": "l2",
                                "engine": "faiss"
                            }
                        },
                    }
                },
            },
        )

    # index data
    vectors = [
        {
            "id": "vec1",
            "values": [0.1, 0.2, 0.3],
            "metadata": {"genre": "drama"},
        },
        {
            "id": "vec2",
            "values": [0.2, 0.3, 0.4],
            "metadata": {"genre": "action"},
        },
    ]

    # bulk insert

    data = ""
    for vector in vectors:
        data += json.dumps({ "index": {"_index": index_name, "_id": vector["id"]} }) + "\n"
        data += json.dumps({i: vector[i] for i in vector if i != "id"}) + "\n"

    client.post(urljoin(endpoint, "/_bulk"), headers=headers, data=data)

    # document by document
    # for vector in vectors:
    #     client.post(urljoin(endpoint, f"/{index_name}/_doc/{vector['id']}"), headers=headers, json=vector)

    # get one of the documents back
    # print(client.get(urljoin(endpoint, f"/{index_name}/_doc/vec1")).json())

    # give it some time to reindex
    time.sleep(1)

    # search
    query = {
        "query": {
            "knn": {
                "values": {
                    "vector": [0.1, 0.2, 0.3],
                    "k": 1,
                    "filter": {
                        "bool": {
                            "must": {
                                "term": {
                                    "metadata.genre": "action"
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    results = client.post(
        urljoin(endpoint, f"/{index_name}/_search"), headers=headers, json=query
    ).json()

    print(results["hits"])

    # delete index
    client.delete(urljoin(endpoint, f"/{index_name}"), headers=headers)


if __name__ == "__main__":
    main()
