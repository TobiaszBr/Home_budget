from rest_framework import status
from django.urls import reverse
import pytest
from expenses.serializers import ExpenseSerializer


class TestExpenseView:
    @pytest.mark.django_db
    def test_create_expense(self, auto_login_user, valid_expense_data):
        client, user = auto_login_user()
        url = reverse("expense-list")
        create_response = client.post(url, data=valid_expense_data, format="json")
        create_response.data.pop("id")
        assert (
                create_response.status_code == status.HTTP_201_CREATED and
                create_response.data == valid_expense_data
        )

    @pytest.mark.django_db
    def test_retrieve_expense(self, django_user_model, auto_login_user, expense_model):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("expense-detail", kwargs={"pk": expense_model.id})
        retrieve_response = client.get(url)

        serializer = ExpenseSerializer(expense_model)
        assert (
                retrieve_response.status_code == status.HTTP_200_OK and
                retrieve_response.data == serializer.data
        )

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "valid_expense_data_update",
        [
            {
                "category": "Savings",
                "subcategory": "Financial cushion",
                "amount": "12.40",
                "description": "Test description 2",
                "date": "2023-02-16"
            },
            {
                "amount": "64.60",
                "description": "Test description 3",
                "date": "2023-04-15"
            },
            {
                "category": "Food",
                "subcategory": "Others",
            },
            {
                "category": "Savings",
            }
        ]
    )
    def test_update_expense_valid_data(
            self,
            django_user_model,
            auto_login_user,
            expense_model,
            valid_expense_data_update
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("expense-detail", kwargs={"pk": expense_model.id})
        update_response = client.patch(url, data=valid_expense_data_update, format="json")
        for key, value in update_response.data.items():
            if key not in valid_expense_data_update.keys():
                valid_expense_data_update[key] = value

        assert (
                update_response.status_code == status.HTTP_200_OK and
                update_response.data == valid_expense_data_update
        )

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "invalid_expense_data_update",
        [
            {
                "subcategory": "Fast food",
            },
            {
                "category": "Food",
            },
            {
                "category": "Food",
                "subcategory": "Investments",
            },
            {
                "amount": "1234567.0",
            },
            {
                "amount": "12345.123",
            },
            {
                "amount": "-21.2",
            }
        ]
    )
    def test_update_expense_invalid_data(
            self,
            django_user_model,
            auto_login_user,
            expense_model,
            invalid_expense_data_update
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("expense-detail", kwargs={"pk": expense_model.id})
        update_response = client.patch(url, data=invalid_expense_data_update, format="json")

        assert update_response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_delete_expense(
            self,
            django_user_model,
            auto_login_user,
            expense_model
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("expense-detail", kwargs={"pk": expense_model.id})
        delete_response = client.delete(url)

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # try to get that owner
        get_response = client.get(url, format="json")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
