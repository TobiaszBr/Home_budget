import sys
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import authentication, generics, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from .models import Expense
from .serializers import ExpenseSerializer, UserSerializer

sys.path.insert(
    0, "C:\\Users\\Switch\\Desktop\\learn\\Home_budget\\home_budget\\report_pdf"
)
from report_pdf_generator import ReportPdf


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
        #if "pk" in self.kwargs.keys():
        try:
            object_instance = self.get_object()
            context["object_instance"] = object_instance
        except:
            pass

        return context

    # "report/(?P<year>[0-9]+)/?(?P<month>[0-9]+)?"
    @action(detail=False, url_path="report/(?P<year>[0-9]+)/?(?P<month>[0-9]+)?")
    def report(self, request, year=None, month=None):
        # Additional year and month validation.
        if int(year) == 0:
            return Response("Year cannot be 0.", status=HTTP_400_BAD_REQUEST)

        if month and (int(month) == 0 or int(month) > 12):
            return Response(
                "Month should be from range 1-12.", status=HTTP_400_BAD_REQUEST
            )

        # Filter database and create response
        if not month:
            q = Q(date__year=year)
            response = dict(year=year)
        else:
            q = Q(date__year=year, date__month=month)
            response = dict(year=year, month=month)
        queryset = self.get_queryset().filter(q).values("category")
        queryset = queryset.annotate(total=Sum("amount"))
        response["data"] = queryset

        # Generate pdf report
        if response["data"]:
            try:
                report_pdf = ReportPdf(response)
                report_pdf.save_pdf()
            except:
                print("Something went wrong with generate pdf file.")
        else:
            print("No data to create pdf report")

        return Response(response)


class UsersListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
