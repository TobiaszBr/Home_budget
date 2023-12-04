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

    endpoint_put = "http://localhost:8000/api/expenses/1/"

    put_data = {
        "category": "Food",
        "subcategory": "Fast food",
        "amount": "443",
        "date": f"2023-11-02",
        "description": f"Test description 2"
    }

    # put response
    put_response = requests.put(endpoint_put, json=put_data, headers=headers)

    pp(put_response.json())
