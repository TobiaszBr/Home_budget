from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve


urlpatterns = [
    path("", include("expenses.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls, name="admin-site"),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT})
]
