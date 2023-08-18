# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from .views import ThongtintaixeApi, Tatcachuyendi
urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path("api/core/thongtintaixe/", ThongtintaixeApi.as_view(), name='hahai_thongtintaixe'),
    path("api/core/tatcachuyendicuataixe/", ThongtintaixeApi.as_view(), name='hahai_tatcachuyendicuataixe'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
