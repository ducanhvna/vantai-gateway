from django.shortcuts import render

from .serializers import CompanySerializer 
from .models import Company 
  
# create a viewset 
class CompanyViewSet(viewsets.ModelViewSet): 
    # define queryset 
    queryset = Company.objects.all() 
      
    # specify serializer to be used 
    serializer_class = CompanySerializer 