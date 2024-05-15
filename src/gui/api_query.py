import requests
import json, os


async def get_api_response(user_query):

    url = os.getenv("ENDPOINT")

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    data = {
        "input": {"question": user_query},
        "config": {},
        "kwargs": {},
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Print the response
    return response.json()["output"]


# output = get_api_response("List the type of Transaction Codes supported for TCS")
# print(output)
