from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import include, path, re_path
from . import views


router = routers.DefaultRouter()
router.register(r"expenses", views.ExpenseViewSet)
router.register(r"reports", views.ReportViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", obtain_auth_token),
    path("users/", views.UsersListAPIView.as_view(), name="users"),
    re_path(
        r"show_report/(?P<year>[0-9]+)(?:/(?P<month>[0-9]+))?",
        views.ShowReportPdfAPIView.as_view(),
        name="show_report"
    ),
]
