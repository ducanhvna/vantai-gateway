from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CompanySerializer 
from .models import Company 
  
# create a viewset 
class CompanyViewSet(APIView): 
    # define queryset 
    queryset = Company.objects.all() 
      
    # specify serializer to be used 
    serializer_class = CompanySerializer 