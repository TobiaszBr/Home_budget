from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions, routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views


# Schema view for swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Budget Management",
      default_version='v1',
      description="Application for budget management – allows adding new "
                  "expenses and generating pdf report based on them.",
      contact=openapi.Contact(email="tobiasz_bernacki@onet.pl"),
      license=openapi.License(name="GNU License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


router = routers.DefaultRouter()
router.register(r"expenses", views.ExpenseViewSet)
router.register(r"reports", views.ReportViewSet)

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/", include(router.urls)),
    path("auth/", obtain_auth_token),
    path("users/", views.UsersListAPIView.as_view(), name="users"),
    path(
        "api/show_report/<int:year>/<int:month>/",
        views.ShowReportPdfAPIViewMonthly.as_view(),
        name="show_report_monthly"
    ),
    path(
        "api/show_report/<int:year>/",
        views.ShowReportPdfAPIViewAnnual.as_view(),
        name="show_report_annual"
    ),
]
