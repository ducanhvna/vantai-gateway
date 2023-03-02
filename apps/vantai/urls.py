from django.urls import path
from .views import vantaihahai_view, UpdatedanhsachmemberWeb, HahaiMemberListView, EditMemberShipView, \
                ChuyendiListView, DeviceListView, DiadiemListView
from django.views.generic import TemplateView
app_name = "apps.vantai"
urlpatterns = [
    path("", vantaihahai_view, name="vantaihahai_view"),
    path('hahaimembers/', HahaiMemberListView.as_view(), name='hahaimember-list'),
    path('updatedanhsachdirect', UpdatedanhsachmemberWeb.as_view(), name  = 'updatedirect'),
    path('tatcachuyendi', ChuyendiListView.as_view(), name= 'tatcachuyendi'),
    path('tatcadiadiem', DiadiemListView.as_view(), name= 'tatcadiadiem'),
    path('devices', DeviceListView.as_view(), name= 'devices'),
    path('edihahaimembership/<int:pk>/', EditMemberShipView.as_view(),name='hahaimembership-update')
]