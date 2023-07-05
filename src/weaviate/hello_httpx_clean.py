#!/usr/bin/env python

import argparse
import json
import time
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
    schema_weaviate_url = endpoint + "/v1/schema"
    object_class = '/Athlete'
    delete_all_obj_url = schema_weaviate_url + object_class

    # Example 8. Delete all objects by removing the schema for object_class
    
    # Connect and get the schema and objects to verify there is something to delete 
    with Client(event_hooks={'request': [log_request],
                            'response': [log_response]}) as client:
        response = client.get(schema_weaviate_url)
    resp_json = response.json()
    classes = resp_json['classes']
    if len(classes) == 0:
        print("Empty Database exiting")
    else: 
        print(delete_all_obj_url)
        with Client(event_hooks={'request': [log_request],
                                 'response': [log_response]}) as client:
            client.delete(delete_all_obj_url)

        # Give enough time to delete all     
        time.sleep(2) 
    
        with Client(event_hooks={'request': [log_request],
                                'response': [log_response]}) as client:
            response = client.get(schema_weaviate_url)
        
        resp_json = response.json()
        classes = resp_json['classes']
        if len(classes) > 0:
            print("Error still exist schema", response['classes'])


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
