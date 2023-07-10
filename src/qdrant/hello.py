#!/usr/bin/env python

from urllib.parse import urljoin
from httpx import Client, Response
import os
from json import dumps


def log_request(request):
    print(f"> {request.method} {request.url}")


def log_response(response):
    request = response.request
    print(f"< {request.method} {request.url} - {response.status_code}")
    if response.status_code >= 299:
        response.read()
        print(f"\n{response.text}")


def main():

    endpoint = os.environ["ENDPOINT"]
    api_key = os.getenv("API_KEY")

    headers = {
        "Accept": "application/json; charset=utf-8",
        "Content-Type": "application/json; charset=utf-8",
        "api-key": api_key
    }

    index_name = "my-index"

    vector = {
        "vectors": {
            "size": 3,
            "distance": "Cosine"
        }
    }

    vectors = [
        {
            "id": 1,
            "vector": [0.1, 0.2, 0.3],
            "payload": {
                "genre": "drama"
            }
        },
        {
            "id": 2,
            "vector": [0.2, 0.3, 0.4],
            "payload": {
                "genre": "action"
            }
        }
    ]

    payload = {"points": vectors}

    with Client(
        event_hooks={
            "request": [log_request],
            "response": [log_response, Response.raise_for_status],
        }
    ) as client:
        client.get(urljoin(endpoint, "/collections"), headers=headers),

        # create the index
        client.put(urljoin(endpoint, "/collections/" + index_name),
                   json=vector, headers=headers)

        # upload vectors
        client.put(urljoin(endpoint,
                       "/collections/" + index_name + "/points?wait=true"),
                       data=dumps(payload), headers=headers)

        # search for data
        query = '{"vector": [0.1,0.2,0.3], "limit": 1}'
        response = client.post(urljoin(endpoint,
                            "/collections/" + index_name + "/points/search"),
                            data=query, headers=headers)
        print(response.json())

        # delete the database
        client.delete(urljoin(endpoint, "/collections/"+ index_name),
                      headers=headers)


if __name__ == "__main__":
    main()
