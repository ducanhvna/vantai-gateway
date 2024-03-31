# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Company 
  
# create a viewset 
class CompanyViewSet(APIView): 
    # define queryset 
    def get(self, request, *args, **kwargs): 
        # result =[]
        # queryset = Company.objects.all() 
        # for item in queryset:
        #     result.append({'id': item.id, 'name': item.name, 'api_version': item.api_version})
        

        # return Response({'count': len(result),'data':result})
        return Response({'count': 0})