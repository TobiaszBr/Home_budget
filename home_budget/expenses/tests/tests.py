from datetime import datetime
import os
from django.db.models import Sum
from django.urls import reverse
import pytest
from rest_framework import status
from expenses.models import Expense, Report
from expenses.serializers import ExpenseSerializer, UserSerializer, ReportSerializer


class TestUserView:
    @pytest.mark.skip
    @pytest.mark.django_db
    def test_list_users_as_admin(self, auto_login_admin_user, user_models):
        client, _ = auto_login_admin_user()
        url = reverse("users")
        list_response = client.get(url)
        assert list_response.status_code == status.HTTP_200_OK

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_list_users_as_non_admin(
        self, django_user_model, auto_login_user, user_models
    ):
        client, _ = auto_login_user(
            user=django_user_model.objects.get(username="User1")
        )
        url = reverse("users")
        list_response = client.get(url)
        assert list_response.status_code == status.HTTP_403_FORBIDDEN


class TestExpenseView:
    @pytest.mark.skip
    @pytest.mark.django_db
    def test_create_expense(self, auto_login_user, valid_expense_data):
        client, user = auto_login_user()
        url = reverse("expense-list")
        create_response = client.post(url, data=valid_expense_data, format="json")
        create_response.data.pop("id")
        assert (
            create_response.status_code == status.HTTP_201_CREATED
            and create_response.data == valid_expense_data
        )

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_retrieve_expense_valid_id(
        self, django_user_model, auto_login_user, expense_model
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("expense-detail", kwargs={"pk": expense_model.id})
        retrieve_response = client.get(url)

        serializer = ExpenseSerializer(expense_model)
        assert (
            retrieve_response.status_code == status.HTTP_200_OK
            and retrieve_response.data == serializer.data
        )

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_retrieve_expense_invalid_id(
        self, django_user_model, auto_login_user, expense_model
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("expense-detail", kwargs={"pk": expense_model.id + 1})
        retrieve_response = client.get(url)

        assert retrieve_response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.skip
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "valid_expense_data_update",
        [
            {
                "category": "Savings",
                "subcategory": "Financial cushion",
                "amount": "12.40",
                "description": "Test description 2",
                "date": "2023-02-16",
            },
            {
                "amount": "64.60",
                "description": "Test description 3",
                "date": "2023-04-15",
            },
            {
                "category": "Food",
                "subcategory": "Others",
            },
            {
                "category": "Savings",
            },
            {
                "subcategory": "Investments",
            },
        ],
    )
    def test_update_expense_valid_data(
        self,
        django_user_model,
        auto_login_user,
        expense_model,
        valid_expense_data_update,
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("expense-detail", kwargs={"pk": expense_model.id})
        update_response = client.patch(
            url, data=valid_expense_data_update, format="json"
        )
        for key, value in update_response.data.items():
            if key not in valid_expense_data_update.keys():
                valid_expense_data_update[key] = value

        assert (
            update_response.status_code == status.HTTP_200_OK
            and update_response.data == valid_expense_data_update
        )

    @pytest.mark.skip
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
            },
        ],
    )
    def test_update_expense_invalid_data(
        self,
        django_user_model,
        auto_login_user,
        expense_model,
        invalid_expense_data_update,
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("expense-detail", kwargs={"pk": expense_model.id})
        update_response = client.patch(
            url, data=invalid_expense_data_update, format="json"
        )

        assert update_response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.skip
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        ("add_to_pk", "expected_status_code"),
        [(0, status.HTTP_204_NO_CONTENT), (1, status.HTTP_404_NOT_FOUND)],
    )
    def test_delete_expense(
        self,
        django_user_model,
        auto_login_user,
        expense_model,
        add_to_pk,
        expected_status_code,
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("expense-detail", kwargs={"pk": expense_model.id + add_to_pk})
        delete_response = client.delete(url)

        assert delete_response.status_code == expected_status_code

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_list_expenses_unauthenticated_user(self, client):
        url = reverse("expense-list")
        list_response = client.get(url)

        assert list_response.status_code == status.HTTP_403_FORBIDDEN


class TestReportView:
    @pytest.mark.skip
    @pytest.mark.parametrize(
        ("year", "month"),
        [
            (datetime.now().year, datetime.now().month),
            (datetime.now().year, None),
        ],
    )
    @pytest.mark.django_db
    def test_create_report_valid_input_data(
        self, django_user_model, auto_login_user, expense_model_list, year, month
    ):
        queryset = Expense.objects.all()
        report_data = queryset.values("category").annotate(total=Sum("amount"))

        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("report-list")
        create_response = client.post(
            url, data={"year": year, "month": month}, format="json"
        )

        instance = Report.objects.get()
        report_delete_path = instance.report_save_path

        assert (
            create_response.status_code == status.HTTP_201_CREATED
            and create_response.data["year"] == year
            and create_response.data["month"] == month
            and all(
                [
                    True
                    for i, element in enumerate(report_data)
                    if create_response.data["data"][i] == report_data[i]
                ]
            )
            and os.path.isfile(report_delete_path)
        )

    @pytest.mark.skip
    @pytest.mark.parametrize(
        ("year", "month"),
        [
            (datetime.now().year + 3000, 1),
            (datetime.now().year - 2000, 1),
            (datetime.now().year, 13),
            (datetime.now().year, 0),
        ],
    )
    @pytest.mark.django_db
    def test_create_report_invalid_input_data(
        self, django_user_model, auto_login_user, expense_model_list, year, month
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("report-list")
        create_response = client.post(
            url, data={"year": year, "month": month}, format="json"
        )

        assert create_response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.skip
    @pytest.mark.parametrize(
        ("year", "month"),
        [
            (datetime.now().year, datetime.now().month),
            (datetime.now().year, None),
        ],
    )
    @pytest.mark.django_db
    def test_create_report_valid_input_data_pdf_already_exists(
        self,
        django_user_model,
        auto_login_user,
        expense_model_list,
        year,
        month,
        report_model,
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("report-list")
        create_response = client.post(
            url, data={"year": year, "month": month}, format="json"
        )

        assert create_response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_retrieve_report_valid_id(
        self, django_user_model, auto_login_user, report_model
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("report-detail", kwargs={"pk": report_model.id})
        retrieve_response = client.get(url)

        serializer = ReportSerializer(report_model)
        assert (
            retrieve_response.status_code == status.HTTP_200_OK
            and retrieve_response.data == serializer.data
        )

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_retrieve_report_invalid_id(
        self, django_user_model, auto_login_user, report_model
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("report-detail", kwargs={"pk": report_model.id + 1})
        retrieve_response = client.get(url)

        assert retrieve_response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_delete_monthly_report(
        self,
        django_user_model,
        auto_login_user,
        report_model_with_pdf_monthly_file
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("report-detail", kwargs={
            "pk": report_model_with_pdf_monthly_file.id
            }
        )
        delete_response = client.delete(url)

        assert (
            delete_response.status_code == status.HTTP_204_NO_CONTENT and not
            os.path.isfile(report_model_with_pdf_monthly_file.report_save_path)
        )

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_delete_annual_report(
        self,
        django_user_model,
        auto_login_user,
        report_model_with_pdf_annual_file
    ):
        client, user = auto_login_user(user=django_user_model.objects.get())
        url = reverse("report-detail", kwargs={
            "pk": report_model_with_pdf_annual_file.id
            }
        )
        delete_response = client.delete(url)

        assert (
            delete_response.status_code == status.HTTP_204_NO_CONTENT and not
            os.path.isfile(report_model_with_pdf_annual_file.report_save_path)
        )

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_list_reports_unauthenticated_user(self, client):
        url = reverse("report-list")
        list_response = client.get(url)

        assert list_response.status_code == status.HTTP_403_FORBIDDEN
