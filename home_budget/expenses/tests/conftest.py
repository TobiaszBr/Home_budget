import pytest
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
        "category": "Food",
        "subcategory": "Fast food",
        "amount": "12.40",
        "description": "Test description",
        "date": "2023-01-02"
    }
    return data

@pytest.fixture
def valid_expense_data_update():
    data = {
        "category": "Savings",
        "subcategory": "Investment",
        "amount": "1020.40",
        "description": "Test description 2",
        "date": "2023-02-04"
    }
    data = {
        "category": "Savings",
        "subcategory": "Investment",
        "amount": "1020.40"
    }
    return data


@pytest.fixture
def expense_model(create_user, valid_expense_data):
    user = create_user(username="User1")
    valid_expense_data["user"] = user
    expense = Expense.objects.create(**valid_expense_data)
    return expense
