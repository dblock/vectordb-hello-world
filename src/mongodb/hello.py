#!/usr/bin/env python

import os
import sys
import time

from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
from pymongo.errors import OperationFailure


def main():
    client = MongoClient(
        os.environ["ENDPOINT"],
        username=os.environ["USERNAME"],
        password=os.environ["PASSWORD"]
    )

    print(f"Connected to MongoDB Atlas {client.server_info()['version']}.")

    db = client["vectordb-hello-world"]
    print(f"Using {db.name}.")

    coll = None
    if not "vectors" in db.list_collection_names():
        print("Creating a collection ...")
        coll = db.create_collection("vectors")
    else:
        coll = db["vectors"]
        coll.delete_many({})

    print(f"Using the {coll.name} collection.")

    model = SearchIndexModel(
        definition={
            "dynamic": True,
            "fields": [
                {
                    "type": "vector",
                    "numDimensions": 3,
                    "path": "values",
                    "similarity": "cosine"
                }
            ]
        },
        name="vector_index",
        type="vectorSearch"
    )

    try:
        print("Creating a search index ...")
        coll.create_search_index(model)
    except OperationFailure:
        pass

    print(f"Waiting for the search index to come online ...", end="")

    vector_index = None
    while not vector_index:
        for index in coll.list_search_indexes():
            print(".", end="")
            sys.stdout.flush()
            if index["name"] == "vector_index":
                if index["status"] == 'READY':
                    vector_index = index
                    break
                elif index["status"] != 'PENDING':
                    print(f"Unexpected index status {index['status']}")
                    break
            time.sleep(3)
    print(f" {vector_index['status']}.")

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

    for vector in vectors:
        coll.insert_one(vector)

    print(f"Inserted {coll.count_documents({})} record(s).")

    print("Searching ...", end="")
    while True:
        results = list(coll.aggregate(
            [
                {
                    '$vectorSearch': {
                        "index": "vector_index",
                        "path": "values",
                        "queryVector": [0.25, 0.3, 0.5],
                        "numCandidates": 5,
                        "limit": 5,
                    }
                }
            ]
        ))

        if len(results) == 0:
            print(".", end="")
            sys.stdout.flush()
            time.sleep(3)
        else:
            print(f" {len(results)} result(s)")
            for result in results:
                print(result)
            break

    print("Cleaning up ...", end="")
    coll.drop_search_index("vector_index")

    while vector_index:
        found = False
        for index in coll.list_search_indexes():
            print(".", end="")
            sys.stdout.flush()
            if index["name"] == "vector_index":
                found = True
                break
        if not found:
            vector_index = None
        else:
            time.sleep(3)

    coll.drop()
    print(" DONE.")


if __name__ == "__main__":
    main()
