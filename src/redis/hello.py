#!/usr/bin/env python

import numpy as np

from redis import Redis
from redis.commands.search.field import TagField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from redis.exceptions import ResponseError


def main():
    r = Redis(host='localhost', port=6379, decode_responses=True)
    # print(r.info()['redis_version'])

    index_name = "vectors"
    doc_prefix = "doc:"

    try:
        schema = (
            TagField("genre"),
            VectorField("values",
                "HNSW", {
                    "TYPE": "FLOAT32", 
                    "DIM": 3, 
                    "DISTANCE_METRIC": "COSINE"
                }
            )
        )

        definition = IndexDefinition(
            prefix=[doc_prefix],
            index_type=IndexType.HASH
        )

        r.ft(index_name).create_index(fields=schema, definition=definition)
    except ResponseError as e:
        if str(e) != 'Index already exists':
            raise e
           
    pipe = r.ft(index_name).pipeline()

    vectors = [
        {
            "id": 1,
            "values": [0.1, 0.2, 0.3],
            "metadata": {"genre": "drama"},
        },
        {
            "id": 2,
            "values": [0.2, 0.3, 0.4],
            "metadata": {"genre": "action"},
        },
    ]

    for vector in vectors:
        key = f"{doc_prefix}{vector['id']}"
        value = {
            "genre": vector["metadata"]["genre"],
            "values": np.array(vector["values"]).astype(np.float32).tobytes() 
        }
        pipe.hset(key, mapping=value)

    pipe.execute()

    # print(doc_prefix)
    # for key in r.scan_iter(f"{doc_prefix}*"):
    #     print(f"  {key}")

    query = (
        Query("(@genre:{ action })=>[KNN 2 @values $vector as score]")
        .sort_by("score")
        .return_fields("id", "score", "genre")
        .dialect(2)
    )

    query_params = {
        "vector": np.array([0.1, 0.2, 0.3]).astype(np.float32).tobytes()
    }

    results = r.ft(index_name).search(query, query_params).docs
    for result in results:
        print(result)

    r.ft(index_name).dropindex(True)

if __name__ == "__main__":
    main()
