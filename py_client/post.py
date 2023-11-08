import requests
from getpass import getpass
from pprint import pprint as pp
from random import randint
from home_budget.expenses.categories import SUBCATEGORIES_DICT


# Authentitacion
auth_endpoint = "http://localhost:8000/api/auth/"
password = "testpassword1"    #getpass()
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
    endpoint = "http://localhost:8000/api/expenses/"

    endpoint_patch = "http://localhost:8000/api/expenses/1/"

    data = {
        "subcategory": "Financial cushion",
    }

    # patch response
    patch_response = requests.patch(endpoint_patch, json=data, headers=headers)

    # post response
    #post_response = requests.post(endpoint, json=data, headers=headers)

    # i = 1
    # for year in range(2019, 2023):
    #     for month in range(1,13):
    #         print(f"------{year} - {month}------")
    #         for category in SUBCATEGORIES_DICT.keys():
    #             day = randint(1, 28)
    #             amount = randint(1, 1000)
    #             subcategory = SUBCATEGORIES_DICT[category][0][0]
    #             # data to POST
    #             data = {
    #                 "category": category,
    #                 "subcategory": subcategory,
    #                 "amount": amount,
    #                 "date": f"{year}-{month}-{day}",
    #                 "description": f"Test description {i}"
    #             }
    #
    #             # POST response
    #             post_response = requests.post(endpoint, json=data, headers=headers)
    #
    #             if post_response.status_code != 201:
    #                 print(data, post_response.json())
    #
    #             print(f"{i}. Status = {post_response.status_code}")
    #             i += 1


    #pp(post_response.json())
