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
    ExpenseReportQuerysetSerializer
)

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

    @action(detail=False, url_path="report/(?P<year>[0-9]+)(?:/(?P<month>[0-9]+))?")
    def report(self, request, year=None, month=None):
        # Additional year and month validation.
        if int(year) <= 0:
            return Response("Year cannot be less than 1.", status=status.HTTP_400_BAD_REQUEST)

        if month and (int(month) <= 0 or int(month) > 12):
            return Response(
                "Month should be from range 1-12.", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            report_instance = Report.objects.get(year=year, month=month)
            serializer = ReportSerializer(report_instance)
        except ObjectDoesNotExist:
            # Filter database and create response:
            if not month:
                q = Q(date__year=year)
            else:
                q = Q(date__year=year, date__month=month)
            queryset = self.get_queryset().filter(q).values("category")
            queryset = queryset.annotate(total=Sum("amount"))
            data = {"year": year, "month": month, "data": queryset}

            # # Generate pdf report
            if queryset:
                try:
                    report_pdf = ReportPdf(data, user=self.request.user)
                    report_pdf.save_pdf()
                    data["report_pdf"] = reverse("show_report", request=request, kwargs={"year": year, "month": month})
                except:
                    print("Something went wrong with generating the pdf file.")
            else:
                data["report_pdf"] = None
                print("No data to create pdf report")

            queryset_serializer = ExpenseReportQuerysetSerializer(queryset, many=True)

            data["data"] = queryset_serializer.data
            serializer = ReportSerializer(data=data)

            # create Report model instance
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=self.request.user)

        return Response(serializer.data)


class ShowReportPdfAPIView(APIView):
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (PDFRendererCustom, JSONRenderer)

    def get(self, request, year, month):
        cwd_path = os.getcwd()
        file_name = f"report_user_id_{self.request.user.id}_{year}_{month}.pdf"
        file_path = os.path.join(cwd_path, "report_pdf", file_name)

        return PDFFileResponse(
            file_path=file_path,
            status=status.HTTP_200_OK
        )


class ReportListAPIView(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)
