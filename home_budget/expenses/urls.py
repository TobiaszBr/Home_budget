from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from . import views


router = routers.DefaultRouter()
router.register(r"expenses", views.ExpenseViewSet)
router.register(r"reports", views.ReportViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", obtain_auth_token),
    path("users/", views.UsersListAPIView.as_view(), name="users"),
    path(
        "show_report/<int:year>/<int:month>/",
        views.ShowReportPdfAPIView.as_view(),
        name="show_report",
    ),
]
