### MongoDB

[MongoDB Atlas](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/) enables semantic, hybrid, generative search, and supports filtering in the serverless version. Sign up on [on their website](https://cloud.mongodb.com/) and create a new database on their free tier. Generate, note the `admin` password, and run the sample as follows.

```
poetry install
USERNAME=... PASSWORD... ENDPOINT=mongodb+srv://vector-cluster.xyz.mongodb.net poetry run ./hello.py

Connected to MongoDB Atlas 7.0.14.
Using vectordb-hello-world.
Creating a collection ...
Using the vectors collection.
Creating a search index ...
Waiting for the search index to come online ... READY.
Inserted 2 record(s).
Searching ........ 2 result(s)
{'_id': ObjectId('671394d5e17d031610d84b2e'), 'id': 'vec2', 'values': [0.2, 0.3, 0.4], 'metadata': {'genre': 'action'}}
{'_id': ObjectId('671394d5e17d031610d84b2d'), 'id': 'vec1', 'values': [0.1, 0.2, 0.3], 'metadata': {'genre': 'drama'}}
Cleaning up ... DONE.
```
