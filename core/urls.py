# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static
from apps.vantai.views import  HanhtrinhImage, EmpImageDisplay
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("vantai/", include("apps.vantai.urls")), # Auth routes - login / register
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path('hanhtrinh', HanhtrinhImage.as_view(), name='home'),
    path('emp-image/<int:pk>/', EmpImageDisplay.as_view(), name='emp_image_display'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # ADD NEW Routes HERE

    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls"))
]

if settings.DEBUG:
    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns