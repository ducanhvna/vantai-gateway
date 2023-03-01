# forms.py 
from django import forms 
from .models import Hanhtrinh, VantaihahaiMembership

class HanhtrinhForm(forms.ModelForm): 
  
    class Meta: 
        model = Hanhtrinh 
        fields = ['name', 'emp_image'] 

class HahaiMembershipForm(forms.ModelForm): 
  
    class Meta: 
        model = VantaihahaiMembership 
        fields = ['device', 'member', 'is_actived'] 

