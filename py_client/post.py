import requests
from getpass import getpass
from pprint import pprint as pp
from random import randint
from home_budget.expenses.categories import SUBCATEGORIES_DICT


# Authentitacion
auth_endpoint = "http://localhost:8000/api/auth/"
password = "testowe1"    #getpass()
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
    endpoint = "http://localhost:8000/api/expenses/"

    i = 0
    for year in range(2019, 2023):
        for month in range(1,13):
            for category in SUBCATEGORIES_DICT.keys():
                day = randint(1, 28)
                amount = randint(1, 1000)
                subcategory = SUBCATEGORIES_DICT[category][0][0]
                # data to POST
                data = {
                    "category": category,
                    "subcategory": subcategory,
                    "amount": amount,
                    "date": f"{year}-{month}-{day}",
                    "description": f"Test description {i}"
                }

                i += 1

                # POST response
                post_response = requests.post(endpoint, json=data, headers=headers)

                print(f"{i}. Status = {post_response.status_code}")
            print(f"------{year} - {month}------")

    #pp(post_response.json())
