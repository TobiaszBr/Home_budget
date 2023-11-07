from rest_framework import status
from django.urls import reverse
import pytest
from expenses.serializers import ExpenseSerializer


class TestExpenseView:
    @pytest.mark.django_db
    def test_create_expense(
            self,
            auto_login_user,
            valid_expense_data
    ):
        client, user = auto_login_user()
        url = reverse("expense-list")
        create_response = client.post(url, data=valid_expense_data, format="json")
        create_response.data.pop("id")
        assert (
                create_response.status_code == status.HTTP_201_CREATED and
                create_response.data == valid_expense_data
        )

    @pytest.mark.django_db
    def test_retrieve_expense(
            self,
            django_user_model,
            auto_login_user,
            expense_model
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("expense-detail", kwargs={"pk": expense_model.id})
        retrieve_response = client.get(url)

        serializer = ExpenseSerializer(expense_model)
        assert (
                retrieve_response.status_code == status.HTTP_200_OK and
                retrieve_response.data == serializer.data
        )





















