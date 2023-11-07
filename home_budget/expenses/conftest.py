import pytest


@pytest.fixture
def client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def test_user_password():
    return "test_password1"


@pytest.fixture
def create_user(db, django_user_model, test_user_password):
    def make_user(**kwargs):
        kwargs["password"] = test_user_password
        user = django_user_model.objects.create_user(**kwargs)
        return user
    return make_user
