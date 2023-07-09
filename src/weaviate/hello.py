from httpx import Client
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

    # HTTPS Setup
    endpoint = os.environ["ENDPOINT"]
    object_weaviate_url = endpoint + "/v1/objects"
    schema_weaviate_url = endpoint + "/v1/schema"
    batch_weaviate_url = endpoint + "/v1/batch/objects"

    # Application Headers
    headers = {
        "Accept": "application/json; charset=utf-8",
        "Content-Type": "application/json; charset=utf-8",
        # "Api-Key": os.environ["API_KEY"],
    }

    # check whether an index exists and print a message
    params = {"fields": "vector"}

    with Client(event_hooks={'request': [log_request],
                             'response': [log_response]}) as client:
        response = client.get(object_weaviate_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if len(data['objects']) == 0:
            print("No objects/index found")
    else:
        print("An error occurred while retrieving vectors from Weaviate.")

    # index data
    vectors = [{
        "id": "vec1",
        "values": [0.1, 0.2, 0.3],
        "properties": {
           "genre": "drama"}
        },
        {
            "id": "vec2",
            "values": [0.2, 0.3, 0.4],
            "properties": {
                "genre": "action"
            }
        }]

    # Create a  few Vectors by adding an objects
    objects = []
    for vector in vectors:
        obj = {
            "class": "Films",
            "properties": {
                "vector": vector["values"]
            }
        }
        objects.append(obj)

    data1 = {"objects": objects}
    with Client(event_hooks={'request': [log_request],
                             'response': [log_response]}) as client:
        client.post(batch_weaviate_url, json=data1, headers=headers)
        client.get(object_weaviate_url)

    params = {"fields": "vector",
              "nearVector": {"vector": [0.1],
                             "certainty": 0.9}}

    with Client(event_hooks={'request': [log_request],
                             'response': [log_response]}) as client:
        response = client.get(object_weaviate_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if len(data['objects']) == 0:
            print("No objects found in the response.")
    else:
        print("An error occurred while retrieving objects from Weaviate.")

    # delete the class for remove all indexes ans objects
    object_class = '/Films'
    class_weaviate_url = schema_weaviate_url + object_class

    with Client(event_hooks={'request': [log_request],
                             'response': [log_response]}) as client:
        response = client.delete(class_weaviate_url)


if __name__ == "__main__":
    main()
