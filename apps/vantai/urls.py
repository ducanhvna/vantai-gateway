from django.urls import path
from .views import vantaihahai_view
from django.views.generic import TemplateView
app_name = "apps.vantai"
urlpatterns = [
    path("", vantaihahai_view, name="vantaihahai_view")
]