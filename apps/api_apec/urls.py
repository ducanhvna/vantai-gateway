from django.urls import path, re_path
from .views import SyncUserDevice
urlpatterns = [
    path("api/apec/syncuser/", SyncUserDevice.as_view(), name='apec_syncuser'),
]