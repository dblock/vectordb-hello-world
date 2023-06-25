#!/usr/bin/env python

import os
import json
from httpx import Client, Response
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
    client = Client(
        verify=False,
        event_hooks={
            "request": [log_request],
            "response": [log_response, Response.raise_for_status],
        },
    )
    headers = {
        "Accept": "application/json; charset=utf-8",
        "Content-Type": "application/json; charset=utf-8",
    }

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
            "metadata": {"genre": "comedy"},
        },
    ]

    for vector in vectors:
        data = json.dumps({"fields": vector})
        client.post(urljoin(endpoint, "/document/v1/vector/vector/docid/" + vector["id"]), headers=headers, data=data)

    # search
    query = "yql=select * from sources * where {targetHits: 1} nearestNeighbor(values,vector_query_embedding)" \
        "&ranking.profile=vector_similarity" \
        "&hits=1" \
        "&input.query(vector_query_embedding)=[0.1,0.2,0.3]"

    results = client.get(
        urljoin(endpoint, "/search/"), headers=headers, params=query
    ).json()
    print(results["root"]["children"][0]["fields"])

    # Delete application
    config_endpoint = os.environ["CONFIG_ENDPOINT"]
    client.delete(urljoin(config_endpoint, "/application/v2/tenant/default/application/default"), headers=headers)

if __name__ == "__main__":
    main()
