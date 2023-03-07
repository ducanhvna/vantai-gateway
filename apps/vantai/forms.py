# forms.py 
from django import forms 
from .models import Hanhtrinh, VantaihahaiMembership, Hanhtrinh, AttackmentHanhTrinh
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class HanhtrinhForm(forms.ModelForm): 
  
    class Meta: 
        model = Hanhtrinh 
        fields = ['name', 'emp_image'] 


class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'


class HahaiMembershipForm(forms.ModelForm): 
  
    class Meta: 
        model = VantaihahaiMembership 
        fields = ['device', 'member', 'is_actived'] 


class HanhtrinhForm(forms.ModelForm):
    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder": "Username",
    #             "class": "form-control"
    #         }
    #     ))
    # email = forms.EmailField(
    #     widget=forms.EmailInput(
    #         attrs={
    #             "placeholder": "Email",
    #             "class": "form-control"
    #         }
    #     ))
    # password1 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "placeholder": "Password",
    #             "class": "form-control"
    #         }
    #     ))
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "placeholder": "Password check",
    #             "class": "form-control"
    #         }
    #     ))
    start_date=forms.DateField(widget=DateInput())
    start_time = forms.TimeField(widget=TimeInput())
    end_date=forms.DateField(widget=DateInput())
    end_time = forms.TimeField(widget=TimeInput())
    
    class Meta:
        model = Hanhtrinh
        fields = ("equipment_id", "product" )
        # widgets = {
        #     'start_date': DateInput(),
        # }


 
class AttackmentForm(forms.ModelForm):
 
    class Meta:
        model = AttackmentHanhTrinh
        fields = ['name','hanhtrinh', 'main_img']