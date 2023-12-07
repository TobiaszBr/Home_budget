from datetime import datetime
from random import randint
from django.contrib.auth import get_user_model
from django.db.models import Sum, Q
import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from typing import Callable, List
from expenses.categories import SUBCATEGORIES_DICT
from expenses.models import Expense, Report
from expenses.serializers import ExpenseReportQuerysetSerializer
from report_pdf_generator import ReportPdf


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def test_user_password() -> str:
    return "test_password1"


@pytest.fixture
def create_user(django_user_model, test_user_password: str) -> Callable:
    def make_user(**kwargs):
        kwargs["password"] = test_user_password
        user = django_user_model.objects.create_user(**kwargs)
        return user

    return make_user


@pytest.fixture
def auto_login_user(
    client: APIClient, create_user: Callable, test_user_password: str
) -> Callable:
    def make_auto_login(user=None):
        if user is None:
            user = create_user(username="User1")
        client.login(username=user.username, password=test_user_password)
        return client, user

    return make_auto_login


@pytest.fixture
def auto_login_admin_user(
    client: APIClient, create_user: Callable, test_user_password: str
) -> Callable:
    def make_auto_login():
        admin_user = create_user(username="admin", is_staff=True)
        client.login(username=admin_user.username, password=test_user_password)
        return client, admin_user

    return make_auto_login


@pytest.fixture
def valid_expense_data() -> dict[str, str]:
    data = {
        "category": "Savings",
        "subcategory": "Investments",
        "amount": "12.40",
        "description": "Test description",
        "date": "2023-01-02",
    }
    return data


@pytest.fixture
def expense_model(create_user: Callable, valid_expense_data: dict[str, str]) -> Expense:
    user = create_user(username="User1")
    valid_expense_data["user"] = user
    expense = Expense.objects.create(**valid_expense_data)
    return expense


@pytest.fixture
def user_models(django_user_model, create_user: Callable) -> List[get_user_model()]:
    user1 = create_user(username="User1")
    user2 = create_user(username="User2")
    users = django_user_model.objects.filter(is_staff=False)
    return users


@pytest.fixture
def valid_expenses_data_list_for_report() -> List[dict[str, str | int]]:
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
                "date": f"{str(datetime.now().year)}-{month}-{day}",
                "description": f"Test description",
            }
            data_list.append(data)

    return data_list


@pytest.fixture
def expense_model_list(
    create_user: Callable,
    valid_expenses_data_list_for_report: List[dict[str, str | int]],
) -> List[Expense]:
    model_list = []
    user = create_user(username="User1")
    for expense_data in valid_expenses_data_list_for_report:
        expense_data["user"] = user
        expense = Expense.objects.create(**expense_data)
        model_list.append(expense)
    return model_list


@pytest.fixture
def report_model(django_user_model, expense_model_list: List[Expense]) -> Report:
    year = datetime.now().year
    month = datetime.now().month
    user = django_user_model.objects.get()

    report_instance = Report.objects.create(
        user=user, year=year, month=None, data=["Dummy"]
    )
    report_instance = Report.objects.create(
        user=user, year=year, month=month, data=["Dummy"]
    )
    return report_instance


@pytest.fixture
def report_model_with_pdf_monthly_file(
    django_user_model, expense_model_list: List[Expense]
) -> Report:
    year = datetime.now().year
    month = datetime.now().month
    q = Q(date__year=year, date__month=month)
    expense_queryset = Expense.objects.filter(q).values("category")
    expense_queryset = expense_queryset.annotate(total=Sum("amount"))
    user = django_user_model.objects.get()
    make_report_data = {"year": year, "month": month, "data": expense_queryset}
    report_pdf = ReportPdf(make_report_data, user=user)
    report_pdf.save_pdf()
    show_report_url = reverse(
        "show_report",
        kwargs={"year": year, "month": month},
    )
    report_save_path = report_pdf.report_save_path

    expense_queryset_serializer = ExpenseReportQuerysetSerializer(
        expense_queryset, many=True
    )
    report_instance = Report.objects.create(
        user=user,
        year=year,
        month=month,
        show_report_url=show_report_url,
        data=expense_queryset_serializer.data,
        report_save_path=report_save_path,
    )
    return report_instance


@pytest.fixture
def report_model_with_pdf_annual_file(
    django_user_model, expense_model_list: List[Expense]
) -> Report:
    year = datetime.now().year
    month = None
    q = Q(date__year=year)
    expense_queryset = Expense.objects.filter(q).values("category")
    expense_queryset = expense_queryset.annotate(total=Sum("amount"))
    user = django_user_model.objects.get()
    make_report_data = {"year": year, "month": month, "data": expense_queryset}
    report_pdf = ReportPdf(make_report_data, user=user)
    report_pdf.save_pdf()
    show_report_url = reverse(
        "show_report",
        kwargs={"year": year, "month": month},
    )
    report_save_path = report_pdf.report_save_path

    expense_queryset_serializer = ExpenseReportQuerysetSerializer(
        expense_queryset, many=True
    )
    report_instance = Report.objects.create(
        user=user,
        year=year,
        month=month,
        show_report_url=show_report_url,
        data=expense_queryset_serializer.data,
        report_save_path=report_save_path,
    )
    return report_instance
