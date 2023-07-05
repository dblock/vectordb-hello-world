#!/usr/bin/env python

import argparse
import json
from httpx import Client


# Print responses
# There are 2 modes controlled by the --verbose argument
# 1. concise for status code and error  
# 2. verbose with dump of data as well 
 
def print_response(r, verbose):
    print(r.url)
    r.read()  
    if r.status_code == 200:
        print("Status code:", r.status_code)
        if verbose:
            if r.request.method != "DELETE":
                formatted_response = json.dumps(r.json(), indent=4)
                print(formatted_response)
    else:
        print("Status code:", r.status_code)
        print("Error message:", json.dumps(r.text, indent=4))
        return None


# Define Global verbose 
# By default no verbose 
verbose = False


# Define Event hooks
def log_request(request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")


def log_response(response):
    request = response.request
    print(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")
    print_response(response, verbose)


def hello_world(endpoint):

    # point to the right URL
    object_weaviate_url = endpoint + "/v1/objects"
    schema_weaviate_url = endpoint + "/v1/schema"
    batch_weaviate_url = endpoint + "/v1/batch/objects"
    query_weaviate_url = endpoint + "/v1/graphql"

    # Application Headers
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    # Connect and get the schema and objects
    with Client(event_hooks={'request': [log_request],
                            'response': [log_response]}) as client:
        client.get(schema_weaviate_url)
        client.get(object_weaviate_url)

    # Class
    class_obj = {
        'class': 'Athlete',
        'vectorizer': 'text2vec-huggingface',
        'properties': [{'name': 'sports',
        'description': 'Name of the sport',
        'dataType': ['text']},
        {'name': 'country', 'description': 'Name of country', 'dataType': ['text']},
        {'name': 'age', 'description': 'age of athlete', 'dataType': ['int']},
        {'name': 'rank', 'description': 'world rank', 'dataType': ['int']},
        {'name': 'points', 'description': 'points', 'dataType': ['int']}]}

    # Data for objects
    athletes = \
    [{'sports': 'Tennis',
    'rank': 1,
    'country': 'Spain',
    'name': 'Carlos Alcaraz',
    'points': 8000,
    'age': 20},
    {'sports': 'Tennis',
    'rank': 2,
    'country': 'Serbia',
    'name': 'Novak Djokovic',
    'points': 7595,
    'age': 36},
    {'sports': 'Tennis',
    'rank': 3,
    'country': 'Russia',
    'name': 'Daniil Medvedev',
    'points': 5890,
    'age': 27},
    {'sports': 'Tennis',
    'rank': 4,
    'country': 'Norway',
    'name': 'Casper Ruud',
    'points': 5490,
    'age': 24},
    {'sports': 'Tennis',
    'rank': 5,
    'country': 'USA',
    'name': 'Amer1',
    'points': 2890,
    'age': 25},
    {'sports': 'Tennis',
    'rank': 6,
    'country': 'USA',
    'name': 'Amer2',
    'points': 1890,
    'age': 25},
    {'sports': 'Soccer',
    'rank': 1,
    'country': 'France',
    'name': 'Mbappe',
    'points': 9890,
    'age': 23},
    {'sports': 'Rugby',
    'rank': 1,
    'country': 'France',
    'name': 'AntoineD',
    'points': 8090,
    'age': 25},
    {'sports': 'Rugby',
    'rank': 1,
    'country': 'England',
    'name': 'Smith',
    'points': 8090,
    'age': 25}]


    # Creation of Objects
    # Example 1. Create a single object
    obj_data = {
        "class": "Athlete",
        "properties": {
            "sports": "Rugby",
            "rank": 1,
            "country": "France",
            "name": "Alldritt",
            "points": 1,
            "age": 26
            }
    }

    with Client(event_hooks={'request': [log_request],
                                'response': [log_response]}) as client:
        client.post(object_weaviate_url, data=json.dumps(obj_data), headers=headers)
        client.get(object_weaviate_url)


    # Example 2. Create a batch and bulk add
    objects = []
    for athlete in athletes:
        obj = {
            "class": class_obj["class"],
            "properties": athlete
        }
        objects.append(obj)

    data1 = {"objects": objects}

    with Client(event_hooks={'request': [log_request],
                            'response': [log_response]}) as client:
        client.post(batch_weaviate_url, json=data1, headers=headers)
        client.get(object_weaviate_url)


    # Example 3. second batch of adds
    athletes2 = [{
        "sports": "Rugby",
        "rank": 1,
        "country": "France",
        "name": "Ntamack",
        "points": 8090,
        "age": 25,
        },
        {"sports": "Rugby",
        "rank": 1,
        "country": "New Zealand",
        "name": "Lomu",
        "points": 8090,
        "age": 53,
        },
        {"sports": "Rugby",
        "rank": 1,
        "country": "France",
        "name": "Penaud",
        "points": 8090,
        "age": 25,
        },
        {"sports": "Rugby",
        "rank": 1,
        "country": "France",
        "name": "Chabal",
        "points": 8090,
        "age": 56,
        }
    ]

    # format data for batch
    objects = []
    for athlete in athletes2:
        obj = {
            "class": class_obj["class"],
            "properties": athlete
        }
        objects.append(obj)

    data2 = {"objects": objects}

    with Client(event_hooks={'request': [log_request],
                                'response': [log_response]}) as client:
        client.post(batch_weaviate_url, json=data2, headers=headers)
        client.get(object_weaviate_url)


    # Queries
    # Example 4. Simple query to get the names of all the players
    # Define the GraphQL query {Get{Athlete{name}}}
    query = """
    {
    Get {
        Athlete {
            name
        }
    }
    }
    """

    with Client(event_hooks={'request': [log_request],
                                    'response': [log_response]}) as client:
        client.post(query_weaviate_url, json={"query": query}, headers=headers)
        client.get(object_weaviate_url)

    # Example 5. Query to get the id of the athlete
    query = """
    {
        Get {
            Athlete {
                age
                country
                name
                points
                rank
                sports
                _additional {
                    id
                }
            }
    }}
    """

    with Client(event_hooks={'request': [log_request],
                                    'response': [log_response]}) as client:
        client.post(query_weaviate_url, json={"query": query}, headers=headers)

    # Example 6. Query to get all rugby player from France
    query = """
    {
    Get {
        Athlete (
        where: {
            operator:And
            operands: [
            {
                operator:Equal,
                path:["sports"],
                valueText:"Rugby"
            },
            {
                operator:Equal,
                path:["country"],
                valueText:"France"
            }
            ]}
        )
        {
        country
        name
        points
        rank
        sports
        }
    }
    }
    """

    with Client(event_hooks={'request': [log_request],
                                    'response': [log_response]}) as client:
        client.post(query_weaviate_url, json={"query": query}, headers=headers)

'''
    # Deletion
    # See hello_httpx_clean.py
'''
 
def main():

    global verbose

    parser = argparse.ArgumentParser(description='Hello Weaviate Python client')
    parser.add_argument('endpoint', help='URL to Weaviate')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
    args = parser.parse_args()

    endpoint = args.endpoint
    verbose = args.verbose

    hello_world(endpoint)


if __name__ == "__main__":
    main()
