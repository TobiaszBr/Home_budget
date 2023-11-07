from rest_framework import status
from django.urls import reverse
import pytest


class TestExpenseView:
    @pytest.mark.django_db
    def test_create_expense(self, client, create_user, test_user_password):
        user = create_user(username="Testowy1")
        client.login(username=user.username, password=test_user_password)

        url = reverse("expense-list")
        data = {
            "category": "Food",
            "subcategory": "Fast food",
            "amount": 12.3,
            "description": "Test description",
        }
        create_response = client.post(url, data=data, format="json")

        assert (
                create_response.status_code == status.HTTP_201_CREATED and
                create_response.data["category"] == data["category"]
        )
























