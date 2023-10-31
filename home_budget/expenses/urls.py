from rest_framework import routers
from django.urls import path, include
from . import views


router = routers.DefaultRouter()
router.register(r"expenses", views.ExpenseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("users/", views.UsersListAPIView.as_view(), name="users")
]
