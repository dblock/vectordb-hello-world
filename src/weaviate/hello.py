#!/usr/bin/env python

from urllib.parse import urljoin

from httpx import Client, Response
import os


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
        "Content-Type": "application/json; charset=utf-8"
    }

    if not api_key is None:
        headers["Authorization"] = f"Bearer {api_key}"

    with Client(
        event_hooks={
            "request": [log_request],
            "response": [log_response, Response.raise_for_status],
        }
    ) as client:
        # index data
        vectors = [
            {
                "id": "vec1",
                "values": [0.1, 0.2, 0.3],
                "properties": { 
                    "genre": "drama"
                }
            },
            {
                "id": "vec2",
                "values": [0.2, 0.3, 0.4],
                "properties": {
                    "genre": "action"
                }
            }
        ]

        objects = []
        for vector in vectors:
            obj = {
                "class": "Vectors",
                "properties": {
                    "vector": vector["values"]
                }
            }
            objects.append(obj)

        client.post(urljoin(endpoint, "/v1/batch/objects"), json={"objects": objects}, headers=headers)
        
        # search for data
        query = {
            "fields": "vector",
            "nearVector": {
                "vector": [0.1],
                "certainty": 0.9
            }
        }

        response = client.get(urljoin(endpoint, "/v1/objects"), params=query, headers=headers).json()
        for obj in response["objects"]:
            print(obj)

        client.delete(urljoin(endpoint, f"/v1/schema/Vectors"), headers=headers)


if __name__ == "__main__":
    main()
