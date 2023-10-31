import requests
from getpass import getpass
from pprint import pprint as pp


# Authentitacion
auth_endpoint = "http://localhost:8000/api/auth/"
password = getpass()
data = {
    "username": "Tobiasz",
    "password": password
}
auth_response = requests.post(auth_endpoint, json=data)

if auth_response.status_code == 200:
    token = auth_response.json()["token"]
    headers = {
        "Authorization": f"Token {token}"
    }
    # Get expenses list
    #endpoint = "http://localhost:8000/api/expenses/"

    # example report
    endpoint = "http://localhost:8000/api/expenses/report/2023/10"

    # GET response
    get_response = requests.get(endpoint, headers=headers)
    pp(get_response.json())
