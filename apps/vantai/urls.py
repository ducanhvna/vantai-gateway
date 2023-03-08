from django.urls import path
from .views import ChitiethanhtrinhView, vantaihahai_view, UpdatedanhsachmemberWeb, HahaiMemberListView, EditMemberShipView, \
                ChuyendiListView, DeviceListView, DiadiemListView, register_user, register_user_for_member, \
                EquipmentListView, MathangListView, hotel_image_view, display_hotel_images, success, \
                CapnhatBatdauHanhtrinhView
from django.views.generic import TemplateView
app_name = "apps.vantai"
urlpatterns = [
    path("", vantaihahai_view, name="vantaihahai_view"),
    path('hahaimembers/', HahaiMemberListView.as_view(), name='hahaimember-list'),
    path('updatedanhsachdirect', UpdatedanhsachmemberWeb.as_view(), name  = 'updatedirect'),
    path('tatcachuyendi', ChuyendiListView.as_view(), name= 'tatcachuyendi'),
    path('tatcadiadiem', DiadiemListView.as_view(), name= 'tatcadiadiem'),
    path('tatcamathang', MathangListView.as_view(), name= 'tatcadiadiem'),
    path('tatcacacxe', EquipmentListView.as_view(), name='tatcacacxe'),
    path('taohanhtrinh', register_user,name="taohanhtrinh"),
    path('regist_for_member/<int:pk>/', register_user_for_member,name='register_user_for_member'),
    path('devices', DeviceListView.as_view(), name= 'devices'),
    path('edihahaimembership/<int:pk>/', EditMemberShipView.as_view(),name='hahaimembership-update'),
    path('batdauhanhtrinh/<int:pk>/', CapnhatBatdauHanhtrinhView.as_view(), name='capnhatbatdau'),
    path('chitiethanhtrinh/<int:pk>/', ChitiethanhtrinhView.as_view(), name='chitiethanhtrinh'),
    path('image_upload', hotel_image_view, name='image_upload'),
    path('hotel_images', display_hotel_images, name = 'hotel_images'),
    path('success', success, name='success'),
]