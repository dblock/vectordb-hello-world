#!/usr/bin/env python

import asyncio
import json

import asyncpg
from asyncpg.exceptions import DuplicateDatabaseError
from pgvector.asyncpg import register_vector


async def main():
    database = "vectors"

    control_connection = await asyncpg.connect(database="template1")

    try:
        server_version = control_connection.get_server_version()
        print(f"PostgreSQL {server_version.major}.{server_version.minor}.{server_version.micro}")

        try:
            await control_connection.execute(f"CREATE DATABASE \"{database}\"")
        except DuplicateDatabaseError:
            pass

        try:
            conn = await asyncpg.connect(database=database)
            await conn.execute(f"CREATE EXTENSION vector")
            await register_vector(conn)

            await conn.execute(f"CREATE TABLE vectors (id text PRIMARY KEY, values vector(3), metadata JSONB)")

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
                q = f"INSERT INTO vectors (id, values, metadata) VALUES($1, $2, $3)"
                await conn.execute(q, vector['id'], vector['values'], json.dumps(vector['metadata']))

            # q = "SELECT * FROM vectors ORDER BY values <-> '[0.2,0.1,0.5]'"
            # results = await conn.fetch(q)
            # for result in results:
            #     print(f"{result} ({json.loads(result['metadata'])['genre']})")
            
            q = "SELECT * FROM vectors WHERE metadata->>'genre' = 'action' ORDER BY values <-> '[0.2,0.1,0.5]'"
            results = await conn.fetch(q)
            for result in results:
                print(f"{result} ({json.loads(result['metadata'])['genre']})")

        finally:
            await conn.close()

    finally:
        await control_connection.execute(f"DROP DATABASE \"{database}\"")
        await control_connection.close()

if __name__ == "__main__":
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop.run_until_complete(main())
  loop.close()