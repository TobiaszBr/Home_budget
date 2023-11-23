import os, sys
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_pdf.response import PDFFileResponse
from rest_framework import authentication, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
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

    def get(self, request, year, month):
        # myślę, że to też niepotrzebne - przekaż w parametrach jakoś może report_save_path???
        cwd_path = os.getcwd()
        file_name = f"report_user_id_{self.request.user.id}_{year}_{month}.pdf"
        file_path = os.path.join(cwd_path, "report_pdf", file_name)

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

        # # Generate pdf report
        if expense_queryset:
            try:
                report_pdf = ReportPdf(make_report_data, user=self.request.user)
                report_pdf.save_pdf()
                show_report_url = reverse(
                    "show_report",
                    request=self.request,
                    kwargs={"year": year, "month": month},
                )
                report_save_path = report_pdf.report_save_path
            except:
                show_report_url = None
                report_save_path = None
                print("Something went wrong with generating the pdf file.")
        else:
            show_report_url = None
            report_save_path = None
            print("No data to create pdf report")

        expense_queryset_serializer = ExpenseReportQuerysetSerializer(
            expense_queryset, many=True
        )
        serializer.save(
            user=self.request.user,
            show_report_url=show_report_url,
            data=expense_queryset_serializer.data,
            report_save_path=report_save_path,
        )

    def perform_destroy(self, instance):
        # Delete also particular report_pdf file
        report_delete_path = instance.report_save_path
        if os.path.isfile(report_delete_path):
            os.remove(report_delete_path)

        instance.delete()
