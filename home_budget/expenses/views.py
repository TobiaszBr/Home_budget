import os
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_pdf.response import PDFFileResponse
from rest_framework import authentication, generics, permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from typing import List
from .decorators import (
    swagger_decorator_expense,
    swagger_decorator_expense_list,
    swagger_decorator_report,
    swagger_decorator_report_list,
    swagger_decorator_show_report_annual,
    swagger_decorator_show_report_monthly
)
from .models import Expense, Report
from .renderers import PDFRendererCustom
from .serializers import (
    ExpenseReportQuerysetSerializer,
    ExpenseSerializer,
    ReportSerializer,
    UserSerializer,
)
from .viewsets import ModelViewSetWithoutEditing
from report_pdf_generator import ReportPdf


class UsersListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


@method_decorator(name="list", decorator=swagger_decorator_expense_list)
@method_decorator(name="retrieve", decorator=swagger_decorator_expense)
@method_decorator(name="update", decorator=swagger_decorator_expense)
@method_decorator(name="partial_update", decorator=swagger_decorator_expense)
@method_decorator(name="destroy", decorator=swagger_decorator_expense)
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "subcategory", "amount", "date", "description"]
    search_fields = ["category", "subcategory", "amount", "date", "description"]
    ordering_fields = ["category", "subcategory", "amount", "date"]

    def perform_create(self, serializer: ExpenseSerializer) -> None:
        serializer.save(user=self.request.user)

    def get_queryset(self) -> List[Expense]:
        return Expense.objects.filter(user=self.request.user)

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        try:
            object_instance = self.get_object()
            context["object_instance"] = object_instance
        except:
            pass
        return context


class ShowReportPdfAPIViewMonthly(APIView):
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (PDFRendererCustom,)

    @swagger_decorator_show_report_monthly
    def get(self, request, year: str = None, month: str = None) -> PDFFileResponse:
        report_instance = get_object_or_404(
            Report, user=self.request.user, year=year, month=month
        )
        file_path = os.path.join(report_instance.report_save_path)

        return PDFFileResponse(file_path=file_path, status=status.HTTP_200_OK)


class ShowReportPdfAPIViewAnnual(APIView):
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (PDFRendererCustom,)

    @swagger_decorator_show_report_annual
    def get(self, request, year: str = None) -> PDFFileResponse:
        report_instance = get_object_or_404(
            Report, user=self.request.user, year=year, month=None
        )
        file_path = os.path.join(report_instance.report_save_path)

        return PDFFileResponse(file_path=file_path, status=status.HTTP_200_OK)


@method_decorator(name="list", decorator=swagger_decorator_report_list)
@method_decorator(name="retrieve", decorator=swagger_decorator_report)
@method_decorator(name="destroy", decorator=swagger_decorator_report)
class ReportViewSet(ModelViewSetWithoutEditing):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["year", "month"]
    search_fields = ["year", "month"]
    ordering_fields = ["year", "month"]

    def get_queryset(self) -> List[Report]:
        return Report.objects.filter(user=self.request.user)

    def perform_create(self, serializer: ReportSerializer) -> None:
        year = self.request.data.get("year", None)
        month = self.request.data.get("month", None)

        # Search for Expenses data to make a report:
        if not month:
            q = Q(date__year=year)
        else:
            q = Q(date__year=year, date__month=month)
        expense_queryset = Expense.objects.filter(q).values("category")
        expense_queryset = expense_queryset.annotate(total=Sum("amount"))
        make_report_data = {"year": year, "month": month, "data": expense_queryset}

        if not expense_queryset:
            raise ValidationError("No expenses data found to create pdf report.")

        # Generate pdf report
        report_pdf = ReportPdf(make_report_data, user=self.request.user)
        report_pdf.save_pdf()
        if month:
            show_report_url = reverse(
                "show_report_monthly",
                request=self.request,
                kwargs={"year": year, "month": month},
            )
        else:
            show_report_url = reverse(
                "show_report_annual",
                request=self.request,
                kwargs={"year": year},
            )

        report_save_path = report_pdf.report_save_path

        expense_queryset_serializer = ExpenseReportQuerysetSerializer(
            expense_queryset, many=True
        )
        serializer.save(
            user=self.request.user,
            show_report_url=show_report_url,
            data=expense_queryset_serializer.data,
            report_save_path=report_save_path,
        )

    def perform_destroy(self, instance: Report) -> None:
        # Delete also particular report_pdf file
        report_delete_path = instance.report_save_path
        if os.path.isfile(report_delete_path):
            os.remove(report_delete_path)

        instance.delete()
