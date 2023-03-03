from django.urls import path
from .views import vantaihahai_view, UpdatedanhsachmemberWeb, HahaiMemberListView, EditMemberShipView, \
                ChuyendiListView, DeviceListView, DiadiemListView, register_user, register_user_for_member
from django.views.generic import TemplateView
app_name = "apps.vantai"
urlpatterns = [
    path("", vantaihahai_view, name="vantaihahai_view"),
    path('hahaimembers/', HahaiMemberListView.as_view(), name='hahaimember-list'),
    path('updatedanhsachdirect', UpdatedanhsachmemberWeb.as_view(), name  = 'updatedirect'),
    path('tatcachuyendi', ChuyendiListView.as_view(), name= 'tatcachuyendi'),
    path('tatcadiadiem', DiadiemListView.as_view(), name= 'tatcadiadiem'),
    path('taohanhtrinh', register_user,name="taohanhtrinh"),
    path('regist_for_member/<int:pk>/', register_user_for_member,name='register_user_for_member'),
    path('devices', DeviceListView.as_view(), name= 'devices'),
    path('edihahaimembership/<int:pk>/', EditMemberShipView.as_view(),name='hahaimembership-update')
]