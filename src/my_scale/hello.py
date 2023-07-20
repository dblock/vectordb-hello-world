#!/usr/bin/env python

import os

from httpx import Client, Response


def log_request(request):
    print(f"> {request.method} {request.url}")
    if request.content:
        print(f"  {request.content.decode('utf-8')}")

def log_response(response):
    request = response.request
    print(f"< {request.method} {request.url} - {response.status_code}")
    if response.status_code >= 299:
        response.read()
        print(f"\n{response.text}")


def main():
    endpoint = os.environ["ENDPOINT"]

    headers = {
        "X-ClickHouse-User": os.environ["USERNAME"],
        "X-ClickHouse-Key": os.environ["PASSWORD"]
    }

    client = Client(
        event_hooks={
            "request": [log_request],
            "response": [log_response, Response.raise_for_status],
        },
    )

    # print(client.post(endpoint, headers=headers, data="SELECT 1").text)

    client.post(endpoint, headers=headers, data=
        "CREATE TABLE IF NOT EXISTS default.vectors (" \
            "id String," \
            "values Array(Float32)," \
            "metadata Map(String, String)," \
            "CONSTRAINT check_length CHECK length(values) = 3," \
            "VECTOR INDEX values_index values TYPE MSTG" \
        ") " \
        "ENGINE = MergeTree " \
        "ORDER BY id"
    )

    try:
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

        for vector in vectors:
            client.post(endpoint, headers=headers, data=
                f"INSERT INTO default.vectors (id, values, metadata) " \
                f"VALUES (\'{vector['id']}\', {vector['values']}, {vector['metadata']})"
            )

        results = client.post(endpoint, headers=headers, data=
            "SELECT * " \
            "FROM default.vectors " \
            "WHERE metadata['genre']='action' " \
            "ORDER BY L2Distance(values, [0.2, 0.3, 0.4])"
        )

        print(results.text)   
    finally:
        client.post(endpoint, headers=headers, data="DROP TABLE default.vectors")

if __name__ == "__main__":
    main()
