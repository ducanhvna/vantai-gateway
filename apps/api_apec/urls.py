from django.urls import path, re_path
from .views import SyncUserDevice, GetListCompany
urlpatterns = [
    path("api/syncuser/", SyncUserDevice.as_view(), name='apec_syncuser'),
    path("api/hrms/listcompany/", GetListCompany.as_view(), name='apec_hrms_company'),
]