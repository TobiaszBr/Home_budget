from getpass import getpass
from pprint import pprint as pp
import requests


# Authentitacion
auth_endpoint = "http://localhost:8000/api/auth/"
password = getpass()
data = {
    "username": "TestUser",
    "password": password
}
auth_response = requests.post(auth_endpoint, json=data)

if auth_response.status_code == 200:
    token = auth_response.json()["token"]
    headers = {
        "Authorization": f"Token {token}"
    }

    patch_data = {
        "category": "Food",
        "subcategory": "Fast food"
    }

    endpoint_patch = "http://localhost:8000/api/expenses/1/"

    # patch response
    patch_response = requests.patch(endpoint_patch, json=patch_data, headers=headers)

    pp(patch_response.json())
