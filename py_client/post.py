from getpass import getpass
from random import randint
import requests
from home_budget.expenses.categories import SUBCATEGORIES_DICT


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
    endpoint_post = "http://localhost:8000/api/expenses/"

    i = 1
    for year in range(2019, 2024):
        for month in range(1,13):
            print(f"------{year} - {month}------")
            for category in SUBCATEGORIES_DICT.keys():
                day = randint(1, 28)
                amount = randint(1, 1000)
                subcategory = SUBCATEGORIES_DICT[category][0]
                # data to POST
                data = {
                    "category": category,
                    "subcategory": subcategory,
                    "amount": amount,
                    "date": f"{year}-{month}-{day}",
                    "description": f"Test description {i}"
                }

                # POST response
                post_response = requests.post(endpoint_post, json=data, headers=headers)

                if post_response.status_code != 201:
                    print(data, post_response.json())

                print(f"{i}. Status = {post_response.status_code}")
                i += 1
else:
    print("Something went wrong - auth?")
    print(auth_response.status_code)
