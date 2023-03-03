# forms.py 
from django import forms 
from .models import Hanhtrinh, VantaihahaiMembership, Hanhtrinh
from bootstrap_datepicker_plus.widgets import DatePickerInput

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
        fields = ('hanhtrinh_id', )
        # widgets = {
        #     'start_date': DateInput(),
        # }
