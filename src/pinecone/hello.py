#!/usr/bin/env python

import os
from httpx import Client, Response
from urllib.parse import urljoin, urlparse


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
    endpoint = urlparse(os.environ["ENDPOINT"])
    controller_endpoint = endpoint._replace(
        netloc=f"controller.{endpoint.netloc}"
    ).geturl()
    index_name = "my-index"
    service_endpoint = endpoint._replace(
        netloc=f'{index_name}-{os.environ["PROJECT_ID"]}.svc.{endpoint.netloc}'
    ).geturl()

    client = Client(
        event_hooks={
            "request": [log_request],
            "response": [log_response, Response.raise_for_status],
        },
    )
    headers = {
        "Accept": "application/json; charset=utf-8",
        "Content-Type": "application/json; charset=utf-8",
        "Api-Key": os.environ["API_KEY"],
    }

    # check whether an index exists
    indices = client.get(
        urljoin(controller_endpoint, "/databases"), headers=headers
    ).json()
    if not index_name in indices:
        client.post(
            urljoin(controller_endpoint, "/databases"),
            headers=headers,
            json={"name": index_name, "dimension": 3},
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

    client.post(
        urljoin(service_endpoint, "/vectors/upsert"),
        headers=headers,
        json={"vectors": vectors, "namespace": "namespace"},
    )

    # search
    results = client.post(
        urljoin(service_endpoint, "/query"),
        headers=headers,
        json={
            "vector": [0.1, 0.2, 0.3],
            "top_k": 1,
            "namespace": "namespace",
            "includeMetadata": True,
        },
    ).json()

    print(results)

    # delete index
    # client.delete(urljoin(controller_endpoint, f"/databases/{index_name}"), headers=headers)


if __name__ == "__main__":
    main()
