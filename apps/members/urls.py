from django.urls import path, re_path
from .views import CompanyViewSet
urlpatterns = [
    path("api/versions/", CompanyViewSet.as_view(), name='api_version'),
]