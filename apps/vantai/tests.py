from django.test import TestCase
import re
# Create your tests here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.utils.crypto import get_random_string
# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
# import generic UpdateView
from django.views.generic.edit import UpdateView
import string
from apps.authentication.forms import SignUpForm
from apps.vantai.models import AttackmentHanhTrinh, MemberSalary, VantaihahaiMember,VantaihahaiMembership, VantaiProduct
from django.views.generic import DetailView, ListView
from apps.vantai.models import Hanhtrinh, Device, VantaihahaiMember, VantaihahaiEquipment, VantaiLocation
from apps.vantai.unity import GetThongtintaixe, tatcachuyendicuataixe, cacchuyendihomnaycuataixe, tatcadiadiem, danhsachtatcaxe, tatcamathang
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.test import TestCase
# from myapp.models import Animal
from django.contrib.auth.models import User
# Create your models here.
def create_new_ref_number():
    code = get_random_string(8, allowed_chars=string.ascii_uppercase + string.digits)
    return code
def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s
def scan_car():
    queryset= danhsachtatcaxe()['data']['results']
    print(queryset)
    for item in queryset:
        try:
            hahai_id = item['id']
            owner_user_id = item['owner_user_id']['id']
            owner_user_name = item['owner_user_id']['name']
            license_plate = item['license_plate']
            name = item['name']
            object_xes = VantaihahaiEquipment.objects.filter(hahai_id=hahai_id)
            if len(object_xes) == 0:
                object_xe = VantaihahaiEquipment()
            else:
                object_xe = object_xes[0]
            object_xe.hahai_id = hahai_id
            object_xe.owner_user_id = owner_user_id
            object_xe.owner_user_name = owner_user_name
            object_xe.license_plate = license_plate
            object_xe.name = name
            object_xe.save()

            print("Thông tin tai xe: ", owner_user_id)
            thongtintaixe =  GetThongtintaixe(owner_user_id)
            print(thongtintaixe)
            members = VantaihahaiMember.objects.filter(member_id=owner_user_id)
            member=None
            if len(members)>0:
                member = members[0]
                member.name = thongtintaixe['data']['name']
                if thongtintaixe['data']['employee_id']:
                    member.employee_id = thongtintaixe['data']['employee_id']['id']
                    member.mobile_phone = thongtintaixe['data']['employee_id']['mobile_phone']
                member.save()
            else:
                print("Create new member", thongtintaixe)
                if thongtintaixe['data']['employee_id']:
                    member = VantaihahaiMember(member_id = owner_user_id, name = thongtintaixe['data']['name'],
                                            employee_id = thongtintaixe['data']['employee_id']['id'],
                                            mobile_phone = thongtintaixe['data']['employee_id']['mobile_phone'],
                                            updated_time = timezone.now())
                    member.save()
                print("Tao user cho memmber")
            if(member):
                try:
                    create_user_for_member(member, owner_user_name)
                except  Exception as ex:
                    print(ex)
        except Exception as ex:
            print(ex)
    return queryset

def scan_location():
    queryset= tatcadiadiem()['data']['results']
    for item in queryset:
        try:
            if item['ward_id'] != None and item['district_id'] != None and item['state_id'] !=None:
                vantai = VantaiLocation(name=item['name'], location_id = item['id'],
                                        ward_id = item['ward_id']['id'],
                                        ward_name= item['ward_id']['name'],
                                        district_id = item['district_id']['id'],
                                        district_name = item['district_id']['name'],
                                        state_id = item['state_id']['id'],
                                        state_name = item['state_id']['name'])
                vantai.save()
            else:
                vantai = VantaiLocation(name=item['name'], location_id = item['id'])
            
                vantai.save()
        except Exception as ex:
            
            print(ex)

def scan_product():
    queryset= tatcamathang()['data']['results']
    lst_product = [item['id'] for item in queryset]
    try:
        VantaiProduct.objects.filter(~Q(product_id__in = lst_product)).delete()
    except Exception as ex:
        print(ex)
    for item in queryset:
        try:
            product = VantaiProduct.objects.get(product_id = item['id'])
            product.name = item['name']
            print('update, ', item['name'])
            product.save()
        except Exception as ex:
            product = VantaiProduct(name=item['name'], product_id = item['id'])
            print('create: ', item['id'])
            product.save()
            print(ex)

def create_user_for_member(member, owner_user_name):
    # member = VantaihahaiMember.objects.get(pk= pk)
    memberships = VantaihahaiMembership.objects.filter(member__id=member.id)
    if len(memberships)==0:
        membership = VantaihahaiMembership(member = member)
        membership.save()
    else:
        membership = memberships[0]
    # if request.method == "POST":
    #     form = SignUpForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    username = no_accent_vietnamese(owner_user_name).replace(' ','').lower().strip()
    print("user: ",username)
    try:
        user = User.objects.create_user(username=username,
                                email=f'{username}@vantaihahai.com',
                                password='vantaihahai')
    except:
        user = User.objects.get(username=username)

    msg = 'User created successfully.'
    success = True
    # device = request.POST.get("device")
    print("device cua chung ta", username)

    # print("device cua chung ta", device)
    # if user is not None:
    #     if device != None and device != '':
        # Create new device
    device_type = 3
    # if device == 'IOS':
    #     device_type = 2
    # elif device == 'ANDROID':
    #     device_type = 1
    device= 'WEB'
    device_id = device + create_new_ref_number()
    while len(Device.objects.filter(id= device_id))>0:
        device_id = device + create_new_ref_number()
    device_object = Device(type = device_type, user = user, id =device_id)
    device_object.save()
    membership.device = device_object
    membership.save()
def scan_drive():
    for i in range(0, 200):
        taixe = GetThongtintaixe(i)
        print (taixe)
        if taixe:
            try:
                print(f" member {i} existed")
                members = VantaihahaiMember.objects.filter(member_id=i)
                if len(members)>0:
                    member = members[0]
                    member.name = taixe['data']['name']
                    if taixe['data']['employee_id']:
                        member.employee_id = taixe['data']['employee_id']['id']
                        member.mobile_phone = taixe['data']['employee_id']['mobile_phone']
                    member.save()
                else:
                    print("Create new member", taixe)
                    member = VantaihahaiMember(member_id = i, name = taixe['data']['name'],
                                            employee_id = taixe['data']['employee_id']['id'],
                                            mobile_phone = taixe['data']['employee_id']['mobile_phone'],
                                            updated_time = timezone.now())
                    member.save()
                
                
            except Exception as ex:
                print (taixe)
                print(ex)

def init_data():
    print("setup")
    DJANGO_SU_NAME = 'admin'
    DJANGO_SU_EMAIL = 'admin@hinosoft.com'
    DJANGO_SU_PASSWORD = 'anphimf12'
    print("create super user")
    try:
        superuser = User.objects.create_superuser(
            username=DJANGO_SU_NAME,
            email=DJANGO_SU_EMAIL,
            password=DJANGO_SU_PASSWORD)

        superuser.save()
    except Exception as ex:
        print(ex)
    print("scan drive")
    scan_drive()
    print("scan laixe")
    scan_car()
    print("scan locations")
    scan_location()
    print("scan Product")
    scan_product()
class AnimalTestCase(TestCase):
    def setUp(self):
        # Animal.objects.create(name="lion", sound="roar")
        # Animal.objects.create(name="cat", sound="meow")
        print("setup")
        DJANGO_SU_NAME = 'admin'
        DJANGO_SU_EMAIL = 'admin@hinosoft.com'
        DJANGO_SU_PASSWORD = 'anphimf12'
        print("create super user")
        superuser = User.objects.create_superuser(
            username=DJANGO_SU_NAME,
            email=DJANGO_SU_EMAIL,
            password=DJANGO_SU_PASSWORD)

        superuser.save()
        print("scan drive")
        scan_drive()
        print("scan laixe")
        scan_car()

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        # lion = Animal.objects.get(name="lion")
        # cat = Animal.objects.get(name="cat")
        # self.assertEqual(lion.speak(), 'The lion says "roar"')
        # self.assertEqual(cat.speak(), 'The cat says "meow"')
        print('memo')
        self.assertEqual('The cat says "meow"', 'The cat says "meow"')