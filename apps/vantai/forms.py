# forms.py 
from django import forms 
from .models import Hanhtrinh
  
class HanhtrinhForm(forms.ModelForm): 
  
    class Meta: 
        model = Hanhtrinh 
        fields = ['name', 'emp_image'] 