# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from .views import ThongtintaixeApi, Tatcachuyendi, Cacchuyenhomnay, CapnhatkmKetthuc, \
                    CapnhatkmBatdau, Danhsachtatcaxe, Thongtinxe, ListYeucaubaotrixe, \
                    TaoghichuBaotri, Danhsachcactinh, ListHuyentheotinh, TatcaDiadiem, \
                    Taohanhtrinh
urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path("api/core/thongtintaixe/", ThongtintaixeApi.as_view(), name='hahai_thongtintaixe'),
    path("api/core/tatcachuyendicuataixe/", Tatcachuyendi.as_view(), name='hahai_tatcachuyendicuataixe'),
    path("api/core/tatcachuyendihomnay/", Cacchuyenhomnay.as_view(), name='hahai_tatcachuyendihomnay'),
    path("api/core/<int:hanhtrinh>/capnhatkmketthuc/", CapnhatkmKetthuc.as_view(), name='hahai_capnhatkmketthuc'),
    path("api/core/<int:hanhtrinh>/capnhatkmbatdau/", CapnhatkmBatdau.as_view(), name='hahai_capnhatkmbatdau'),
    path("api/core/danhsachtatcaxe/", Danhsachtatcaxe.as_view(), name='hahai_danhsachtatcaxe'),
    # Matches any html file
    path("api/core/<int:equitment>/thongtinxe/", Thongtinxe.as_view(), name="hahai_thongtinxe"),

    path("api/core/<int:equitment>/danhsachyeucaubaotri/", ListYeucaubaotrixe.as_view(), name="list_yeucaubaotri"),
    path("api/core/<int:equitment>/taoghichu/", TaoghichuBaotri.as_view(), name="capnhat_ghichubaotri"),
    path("api/core/danhsachcactinh/", Danhsachcactinh.as_view(), name="list_tinh"),
    path("api/core/<int:province>/danhsachcachuyen/", ListHuyentheotinh.as_view(), name="list_huyen"),
    # district
    path("api/core/<int:district>/danhsachcacphuong/", ListHuyentheotinh.as_view(), name="list_phuong"),
    path("api/core/danhsachcacdiadiem/", TatcaDiadiem.as_view(), name="list_diadiem"),

    path("api/core/<int:equitment>/taohanhtrinh/", Taohanhtrinh.as_view(), name="hahai_taohanhtrinh"),
    re_path(r'^.*\.*', views.pages, name='pages'),
]
