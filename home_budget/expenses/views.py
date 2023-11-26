import os, sys
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_pdf.response import PDFFileResponse
from rest_framework import authentication, generics, permissions, status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .models import Expense, Report
from .renderers import PDFRendererCustom
from .serializers import (
    ExpenseSerializer,
    UserSerializer,
    ReportSerializer,
    ExpenseReportQuerysetSerializer,
)
from .viewsets import ModelViewSetWithoutEditing


# ToDo and check
sys.path.insert(
    0, "C:\\Users\\Switch\\Desktop\\learn\\Home_budget\\home_budget\\report_pdf"
)
from report_pdf_generator import ReportPdf

# ToDo and check


class UsersListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            object_instance = self.get_object()
            context["object_instance"] = object_instance
        except:
            pass

        return context


class ShowReportPdfAPIView(APIView):
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (PDFRendererCustom,)

    def get(self, request, year=None, month=None):
        report_instance = get_object_or_404(
            Report, user=self.request.user, year=year, month=month
        )
        file_path = os.path.join(report_instance.report_save_path)

        return PDFFileResponse(file_path=file_path, status=status.HTTP_200_OK)


class ReportViewSet(ModelViewSetWithoutEditing):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
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

        try:
            # Generate pdf report
            report_pdf = ReportPdf(make_report_data, user=self.request.user)
            report_pdf.save_pdf()
            show_report_url = reverse(
                "show_report",
                request=self.request,
                kwargs={"year": year, "month": month},
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
        except:
            raise APIException(
                "Something went wrong with generating the pdf file."
                " Report instance will not be saved."
            )

    def perform_destroy(self, instance):
        # Delete also particular report_pdf file
        report_delete_path = instance.report_save_path
        if os.path.isfile(report_delete_path):
            os.remove(report_delete_path)

        instance.delete()
