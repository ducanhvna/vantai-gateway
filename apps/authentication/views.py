# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from apps.devices.models import Device
from django.utils.crypto import get_random_string
import string

# Create your models here.
def create_new_ref_number():
    code = get_random_string(8, allowed_chars=string.ascii_uppercase + string.digits)
    return code

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created successfully.'
            success = True
            device = request.POST.get("device")
            print("device cua chung ta", username)

            print("device cua chung ta", device)
            if user is not None:
                if device != None and device != '':
                # Create new device
                    device_type = 3
                    if device == 'IOS':
                        device_type = 2
                    elif device == 'ANDROID':
                        device_type = 1
                    
                    device_id = device + create_new_ref_number()
                    while len(Device.objects.filter(id= device_id))>0:
                        device_id = device + create_new_ref_number()
                    device_object = Device(type = device_type, user = user, id =device_id)
                    device_object.save()

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
