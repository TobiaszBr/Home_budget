from random import randint
import pytest
from expenses.categories import SUBCATEGORIES_DICT
from expenses.models import Expense


@pytest.fixture
def client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def test_user_password():
    return "test_password1"


@pytest.fixture
def create_user(django_user_model, test_user_password):
    def make_user(**kwargs):
        kwargs["password"] = test_user_password
        user = django_user_model.objects.create_user(**kwargs)
        return user

    return make_user


@pytest.fixture
def auto_login_user(client, create_user, test_user_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user(username="User1")
        client.login(username=user.username, password=test_user_password)
        return client, user

    return make_auto_login


@pytest.fixture
def valid_expense_data():
    data = {
        "category": "Savings",
        "subcategory": "Investments",
        "amount": "12.40",
        "description": "Test description",
        "date": "2023-01-02",
    }
    return data


@pytest.fixture
def expense_model(create_user, valid_expense_data):
    user = create_user(username="User1")
    valid_expense_data["user"] = user
    expense = Expense.objects.create(**valid_expense_data)
    return expense


@pytest.fixture
def valid_expenses_data_list_for_report():
    data_list = []
    for month in range(1, 13):
        for category in SUBCATEGORIES_DICT.keys():
            day = randint(1, 28)
            amount = randint(1, 1000)
            subcategory = SUBCATEGORIES_DICT[category][0][0]

            data = {
                "category": category,
                "subcategory": subcategory,
                "amount": amount,
                "date": f"2023-{month}-{day}",
                "description": f"Test description"
            }
            data_list.append(data)

    return data_list


@pytest.fixture
def expense_model_list(create_user, valid_expenses_data_list_for_report):
    model_list = []
    user = create_user(username="User1")
    for expense_data in valid_expenses_data_list_for_report:
        expense_data["user"] = user
        expense = Expense.objects.create(**expense_data)
        model_list.append(expense)
    return model_list
