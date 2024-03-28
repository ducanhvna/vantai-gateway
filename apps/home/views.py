# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime, timezone
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from apps.devices.models import Device
from apps.vantai.models import AttackmentHanhTrinh, Hanhtrinh, VantaihahaiEquipment, VantaihahaiMember, VantaihahaiMembership
from apps.vantai.unity import cacchuyendihomnaycuataixe, chitiethanhtrinh, tatcachuyendicuataixe, \
    GetThongtintaixe, danhsachtatcaxe, VanTaiHaHai, tatcamathang, thongtinxe, danhsachyeucaubaotrixe, capnhatghichubaotri, \
    danhsachcacphuongtheohuyen, danhsachcachuyentheotinh, danhsachcactinh, tatcadiadiem, themmoichuyendi
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

import string
from apps.vantai.models import VantaiLocation, Hanhtrinh, VantaihahaiMember
# Create your models here.
def create_new_ref_number():
    code = get_random_string(8, allowed_chars=string.ascii_uppercase + string.digits)
    return code

@login_required(login_url="/login/")
def index(request):
    # chuyendi = cacchuyendihomnaycuataixe(4)
    chuyendi= tatcachuyendicuataixe(4)
    print(chuyendi)
    print('abc',request.user)
    queryset = []
    # find device
    devices = Device.objects.filter(user=request.user)
    # if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
    #     queryset = self.model.objects.filter(
    #         Q(assign_to=self.request.user)).annotate(num_asins=Count('pod_asins'), 
    #         num_completed = Count('pod_asins', filter=Q(pod_asins__completed=True)),
    #         num_reviewed = Count('pod_asins', filter=~Q(pod_asins__review_by=None)))
    # else :
    #     queryset = self.model.objects.annotate(num_asins=Count('pod_asins'), 
    #         num_completed = Count('pod_asins', filter=Q(pod_asins__completed=True)),
    #         num_reviewed = Count('pod_asins', filter=~Q(pod_asins__review_by=None)))
    # # return queryset.prefetch_related("contacts", "account")
    results= []
    if len(devices)>0:
        device = devices[0]
        memberships = VantaihahaiMembership.objects.filter(device=device)
        if len(memberships) >0:
            membership = memberships[0]
            member = membership.member
            employee_id = member.employee_id
            print("Tat ca cac chuyen di cua: ", employee_id)
            queryset= tatcachuyendicuataixe(employee_id)['data']['results']
            print(queryset)
            
            for item in queryset:
                try:
                    hanhtrinh= None
                    hanhtrinh_list = Hanhtrinh.objects.filter(hanhtrinh_id=item['id'])
                    if len(hanhtrinh_list)>0:
                        hanhtrinh= hanhtrinh_list[0]
                    else:
                        hanhtrinh= Hanhtrinh()
                    if hanhtrinh:
                        hanhtrinh.employee_id = employee_id
                        print("employee: ", employee_id)
                        hanhtrinh.hanhtrinh_id = item['id']
                        hanhtrinh.equipment_id = item['equipment_id']['id']
                        hanhtrinh.license_plate = item['equipment_id']['license_plate']
                        hanhtrinh.name = item['equipment_id']['name']
                        hanhtrinh.schedule_date = datetime.strptime(item['schedule_date'], "%Y-%m-%d")
                        hanhtrinh.location_name = item['location_name']
                        hanhtrinh.location_dest_name = item['location_dest_name']
                        hanhtrinh.odo_start = item['odometer_start']
                        # hanhtrinh.odo_end = item['odometer_dest']
                        if item['ward_id']:
                            hanhtrinh.ward_id  = item['ward_id']
                        hanhtrinh.save()
                        
                        attachments = item['attachment_ids']
                        for attachment in attachments:
                            AttackmentHanhTrinh.objects.get_or_create(hanhtrinh=hanhtrinh, main_img=attachment['url'])
                    if hanhtrinh.id:
                        results.append(hanhtrinh)
                except Exception as ex:
                    print('sync chuyen di err: ', ex)
    # else:        
        # queryset= Hanhtrinh.objects.filter(employee_id = employee_id).order_by('-schedule_date', '-created_time')
    print(queryset)
    

    context = {'segment': 'index', 'joyneys' : results}
    
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

class CreateDevice(APIView):
    def post(self, request, format=None):
        device_id = request.data.get('id')
        device_type = request.data.get('type')
        
        devices = Device.objects.filter(id=device_id)
        
        if len(devices) == 0:
            code = create_new_ref_number()
            while len(user.objects.filter(username=code)) > 0:
                code = create_new_ref_number()
            print('code: ',code)
            # device_id = request.data.get('id')
            user = User.objects.create_user(username=code,
                                    email=f'{code}@vantaihahai.com',
                                    password=code)
            # serializer.save(user= user, name=code)
            # user_profile = UserProfile(user_id=user.id,
            #                            affiliate_code=''.join(
            #                                random.choices(string.ascii_uppercase + string.digits, k=8)))
            # user_profile.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            vantai = VanTaiHaHai()
            member_id = vantai.create_employee(code)
            vantai_object = VantaihahaiMember()
            vantai_object.member_id = member_id
            vantai_object.name = code
            
            device = Device(device_type = device_type, id=id, user= user)
            memberships = VantaihahaiMembership.objects.filter(device = device, member = vantai_object)

            # if len(memberships)>0:
            #     membership = memberships[0]
            #     hahai_member = membership.member
            # print("tim kiem xe cua member_id: ",hahai_member.member_id)
            # xe_phutrachs = VantaihahaiEquipment.objects.filter(owner_user_id= hahai_member.member_id)
            # if len(xe_phutrachs)>0:
            #     xe_phutrach = xe_phutrachs[0]
            return Response(device)
                
        id = request.data.get('id')
        type = request.data.get('type')
        return Response(devices)
        # try to read existed
        # try:
        #     device = Device.objects.get(id=id, type=type)
        #     if device:
        #         serializer = DeviceSerializer(device)
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        # except:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ThongtintaixeApi(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, *args, **kwargs): 
        
        try:
            # user = self.request.user 
            devices = Device.objects.filter(user=self.request.user)
            print("danh sach : ",devices)
            # device = user.user_device
            if len(devices)>0:
                device = devices[0]
            # if device:
                data = GetThongtintaixe(device.device_membership.member.member_id)
                data['data']['code'] = device.name
                # salaries = MemberSalary.objects.filter(member = device.device_membership.member)
                # ls = []
                # for item in salaries:
                #     ls.append({'date':item.date, 'salary':item.salary})
                # data['data']['salary'] = ls

                return Response(data)

            return Response({
                            'status': False, 
                            'error' : "You does not own any device, please create a new one"
                        })
        except Exception as ex:
            print(ex)
            return Response({
                            'status': False, 
                            'error' : "You does not own any device, please create a new one"
                        })
        
class Tatcachuyendi(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, *args, **kwargs): 
        # try:
        queryset = []
        results= []
        # find device
        devices = Device.objects.filter(user=self.request.user)
        # if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
        #     queryset = self.model.objects.filter(
        #         Q(assign_to=self.request.user)).annotate(num_asins=Count('pod_asins'), 
        #         num_completed = Count('pod_asins', filter=Q(pod_asins__completed=True)),
        #         num_reviewed = Count('pod_asins', filter=~Q(pod_asins__review_by=None)))
        # else :
        #     queryset = self.model.objects.annotate(num_asins=Count('pod_asins'), 
        #         num_completed = Count('pod_asins', filter=Q(pod_asins__completed=True)),
        #         num_reviewed = Count('pod_asins', filter=~Q(pod_asins__review_by=None)))
        # # return queryset.prefetch_related("contacts", "account")
        if len(devices)>0:
            device = devices[0]
            memberships = VantaihahaiMembership.objects.filter(device=device)
            if len(memberships) >0:
                membership = memberships[0]
                member = membership.member
                employee_id = member.employee_id
                print("Tat ca cac chuyen di cua: ", employee_id)
                queryset= tatcachuyendicuataixe(employee_id)
                queryset2= VanTaiHaHai().tatcachuyendicuataixe(employee_id)
                for item in queryset['data']['results']:
                    for item2 in queryset2['data']['results']:
                        if (item['id'] == item2['id']):
                            item['location_id'] = item2['location_id']
                            item['location_dest_id'] = item2['location_dest_id']
                print(queryset)
                # lst_htrinh = [item['id'] for item in queryset['data']['results']]
                # Hanhtrinh.objects.filter(~Q(hanhtrinh_id__in = lst_htrinh)).delete()
                # for item in queryset['data']['results']:
                #     # try:
                #     hanhtrinh= None
                #     hanhtrinh_list = Hanhtrinh.objects.filter(hanhtrinh_id=item['id'])
                #     if len(hanhtrinh_list)>0:
                #         hanhtrinh= hanhtrinh_list[0]
                #     else:
                #         hanhtrinh= Hanhtrinh()
                #     if hanhtrinh:
                #         hanhtrinh.employee_id = employee_id
                #         print("employee: ", employee_id)
                        
                #         hanhtrinh.hanhtrinh_id = item['id']
                #         hanhtrinh.equipment_id = item['equipment_id']['id']
                #         hanhtrinh.license_plate = item['equipment_id']['license_plate']
                #         hanhtrinh.name = item['equipment_id']['name']
                #         try:
                #             hanhtrinh.schedule_date = datetime.datetime.strptime(item['schedule_date'], "%Y-%m-%d")
                #         except Exception as ex:
                #             print(item['schedule_date'])
                #             print(ex)
                #         hanhtrinh.location_name = item['location_name']
                #         hanhtrinh.location_dest_name = item['location_dest_name']
                #         hanhtrinh.odo_start = item['odometer_start']
                #         # hanhtrinh.odo_end = item['odometer_dest']
                #         if item['ward_id']:
                #             hanhtrinh.ward_id  = item['ward_id']
                #         hanhtrinh.save()
                #         # item['sid'] = item['id']
                #         # item['id'] = hanhtrinh.pk
                #         attachments = item['attachment_ids']
                #         for attachment in attachments:
                #             AttackmentHanhTrinh.objects.get_or_create(hanhtrinh=hanhtrinh, main_img=attachment['url'])
                    # if hanhtrinh.id:
                    #     results.append(hanhtrinh)
                    # except Exception as ex:
                    #     return Response({
                    #         'status': False, 
                    #         'error' : "sync chuyen di err"
                    #     })
        return Response(queryset)
        # except Exception as ex:
        #     print(ex)
        #     return Response({
        #                     'status': False, 
        #                     'error' : "You does not own any device, please create a new one"
        #                 })

class Cacchuyenhomnay(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, *args, **kwargs): 
        queryset = []
        results= []
        # find device
        devices = Device.objects.filter(user=self.request.user)
        # if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
        #     queryset = self.model.objects.filter(
        #         Q(assign_to=self.request.user)).annotate(num_asins=Count('pod_asins'), 
        #         num_completed = Count('pod_asins', filter=Q(pod_asins__completed=True)),
        #         num_reviewed = Count('pod_asins', filter=~Q(pod_asins__review_by=None)))
        # else :
        #     queryset = self.model.objects.annotate(num_asins=Count('pod_asins'), 
        #         num_completed = Count('pod_asins', filter=Q(pod_asins__completed=True)),
        #         num_reviewed = Count('pod_asins', filter=~Q(pod_asins__review_by=None)))
        # # return queryset.prefetch_related("contacts", "account")
        if len(devices)>0:
            device = devices[0]
            memberships = VantaihahaiMembership.objects.filter(device=device)
            if len(memberships) >0:
                membership = memberships[0]
                member = membership.member
                employee_id = member.employee_id
                result = cacchuyendihomnaycuataixe(employee_id)
                for item in result['data']['results']:
                    # try:
                    hanhtrinh= None
                    hanhtrinh_list = Hanhtrinh.objects.filter(hanhtrinh_id=item['id'])
                    if len(hanhtrinh_list)>0:
                        hanhtrinh= hanhtrinh_list[0]
                    else:
                        hanhtrinh= Hanhtrinh()
                    if hanhtrinh:
                        hanhtrinh.employee_id = employee_id
                        print("employee: ", employee_id)
                        hanhtrinh.hanhtrinh_id = item['id']
                        hanhtrinh.equipment_id = item['equipment_id']['id']
                        hanhtrinh.license_plate = item['equipment_id']['license_plate']
                        hanhtrinh.name = item['equipment_id']['name']
                        try:
                            hanhtrinh.schedule_date = datetime.datetime.strptime(item['schedule_date'], "%Y-%m-%d")
                        except Exception as ex:
                            print(item['schedule_date'])
                            print(ex)
                        hanhtrinh.location_name = item['location_name']
                        hanhtrinh.location_dest_name = item['location_dest_name']
                        hanhtrinh.odo_start = item['odometer_start']
                        # hanhtrinh.odo_end = item['odometer_dest']
                        if item['ward_id']:
                            hanhtrinh.ward_id  = item['ward_id']
                        hanhtrinh.save()
                        # item['sid'] = item['id']
                        # item['id'] = hanhtrinh.pk
                        attachments = item['attachment_ids']
                        for attachment in attachments:
                            AttackmentHanhTrinh.objects.get_or_create(hanhtrinh=hanhtrinh, main_img=attachment['url'])
                return Response(result)
            # except Exception as ex:
            #     print(ex)
            #     return Response({
            #                     'status': False, 
            #                     'error' : "You does not own any device, please create a new one"
            #                 })

    

class CapnhatkmKetthuc(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def put(self, request, *args, **kwargs): 
        hanhtrinh = kwargs.get('hanhtrinh')
        km_end = request.data.get('km')
        url = request.data.get('url')
        # attackements = request.data.get('attackements')
        attackements = [url]
        # ht_object = Hanhtrinh.objects.get(hanhtrinh_id=hanhtrinh)
        # ht_object.odo_end= km_end
        # ht_object.save()
        vantai = VanTaiHaHai()
        vantai.capnhatsokmketthuchanhtrinh(hanhtrinh, km_end, None, attackements)
            # attachments = body['attachments']
            # for item in attachments:
            #     atts= AttackmentHanhTrinh.objects.filter(hanhtrinh = ht_object, url=item)
            #     if len(atts) == 0:
            #         att = AttackmentHanhTrinh(hanhtrinh = ht_object, url= item)
            #         att.save()

        result = chitiethanhtrinh(hanhtrinh)
        # result['data']['sid'] = result['data']['id']
        # result['data']['id'] = ht_object.pk
        return Response(result)
        # except Exception as ex:
        #     print(ex)
        #     return Response({
        #                     'status': False, 
        #                     'error' : "You does not own any device, please create a new one"
        #                 })
        #     vantai = VanTaiHaHai()
        #     vantai.capnhatsokmketthuchanhtrinh(hanhtrinh.hanhtrinh_id, odo_end, body, attackements)
        #     return HttpResponseRedirect('/vantai/chitiethanhtrinh/{}/'.format(hanhtrinh.id))

        # context = self.get_context_data(form=form)
        # return self.render_to_response(context)     
    # def get_context_data(self, **kwargs):
    #     """Overide get_context_data method
    #     """
        
    #     context = super(CapnhatKetthucHanhtrinhView, self).get_context_data(**kwargs)
    #     hanhtrinh_pk = self.kwargs['pk']
    #     hanhtrinh = Hanhtrinh.objects.get(pk=hanhtrinh_pk)
    #     form = KmHanhtrinhForm(initial={'name':f"End-{hanhtrinh.hanhtrinh_id}",'odo':None,'hanhtrinh': hanhtrinh})  # instance= None

    #     context["form"] = form
    #     #context["latest_article"] = latest_article

    #     return context
    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)
class CapnhatDiadiemBatdau(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def put(self, request, *args, **kwargs): 
        hanhtrinh = kwargs.get('hanhtrinh')
        location_id = request.data.get('location_id')
        # ht_object = Hanhtrinh.objects.get(hanhtrinh_id=hanhtrinh)
        # ht_object.odo_start= km_end
        # ht_object.save()
        vantai = VanTaiHaHai()
        vantai.capnhatlocationbatdauhanhtrinh(hanhtrinh, location_id)
            # attachments = body['attachments']
            # for item in attachments:
            #     atts= AttackmentHanhTrinh.objects.filter(hanhtrinh = ht_object, url=item)
            #     if len(atts) == 0:
            #         att = AttackmentHanhTrinh(hanhtrinh = ht_object, url= item)
            #         att.save()
        result = chitiethanhtrinh(hanhtrinh)
        # result['data']['sid'] = result['data']['id']
        # result['data']['id'] = ht_object.pk
        return Response(result)
class CapnhatDiadiemKetthuc(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def put(self, request, *args, **kwargs): 
        hanhtrinh = kwargs.get('hanhtrinh')
        location_id = request.data.get('location_id')
        # ht_object = Hanhtrinh.objects.get(hanhtrinh_id=hanhtrinh)
        # ht_object.odo_start= km_end
        # ht_object.save()
        vantai = VanTaiHaHai()
        vantai.capnhatlocationketthuchanhtrinh(hanhtrinh, location_id)
            # attachments = body['attachments']
            # for item in attachments:
            #     atts= AttackmentHanhTrinh.objects.filter(hanhtrinh = ht_object, url=item)
            #     if len(atts) == 0:
            #         att = AttackmentHanhTrinh(hanhtrinh = ht_object, url= item)
            #         att.save()
        result = chitiethanhtrinh(hanhtrinh)
        # result['data']['sid'] = result['data']['id']
        # result['data']['id'] = ht_object.pk
        return Response(result)
class CapnhatkmBatdau(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def put(self, request, *args, **kwargs): 
        hanhtrinh = kwargs.get('hanhtrinh')
        km_end = request.data.get('km')
        # attackements = request.data.get('attackements')
        attackements = []
        # ht_object = Hanhtrinh.objects.get(hanhtrinh_id=hanhtrinh)
        # ht_object.odo_start= km_end
        # ht_object.save()
        vantai = VanTaiHaHai()
        vantai.capnhatsokmbatdauhanhtrinh(hanhtrinh, km_end, None, attackements)
            # attachments = body['attachments']
            # for item in attachments:
            #     atts= AttackmentHanhTrinh.objects.filter(hanhtrinh = ht_object, url=item)
            #     if len(atts) == 0:
            #         att = AttackmentHanhTrinh(hanhtrinh = ht_object, url= item)
            #         att.save()
        result = chitiethanhtrinh(hanhtrinh)
        # result['data']['sid'] = result['data']['id']
        # result['data']['id'] = ht_object.pk
        return Response(result)
class DanhsachMathang(APIView): 
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs): 
        queryset= tatcamathang()
        
        return Response(queryset)
        
class Danhsachtatcaxe(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, *args, **kwargs): 
        queryset= danhsachtatcaxe()
        print(queryset['data']['results'])
        for item in queryset['data']['results']:
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
            # item['sid'] = item['id']
            # item['id'] = object_xe.pk

            # print("Thông tin tai xe: ", owner_user_id)
            # thongtintaixe =  GetThongtintaixe(owner_user_id)
            # print(thongtintaixe)
            # members = VantaihahaiMember.objects.filter(member_id=owner_user_id)
            # if len(members)>0:
            #     member = members[0]
            #     member.name = thongtintaixe['data']['name']
            #     if thongtintaixe['data']['employee_id']:
            #         member.employee_id = thongtintaixe['data']['employee_id']['id']
            #         member.mobile_phone = thongtintaixe['data']['employee_id']['mobile_phone']
            #     member.save()
            # else:
            #     print("Create new member", thongtintaixe)
            #     if thongtintaixe['data']['employee_id']:
            #         member = VantaihahaiMember(member_id = owner_user_id, name = thongtintaixe['data']['name'],
            #                                 employee_id = thongtintaixe['data']['employee_id']['id'],
            #                                 mobile_phone = thongtintaixe['data']['employee_id']['mobile_phone'],
            #                                 updated_time = timezone.now())
            #         member.save()
        
        return Response(queryset)
    
class Thongtinxe(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, *args, **kwargs): 
        equitment_id = kwargs.get('equitment')
        ht_object = VantaihahaiEquipment.objects.get(hahai_id=equitment_id)
        # user = request.user 
        try:
            # device = user.user_device
        # if device:
            
            result = thongtinxe(ht_object.hahai_id)
            # result['data']['sid'] = result['data']['id']
            # result['data']['id'] = ht_object.pk
            return Response(result)
        except Exception as ex:
            print(ex)
            return Response({
                            'status': False, 
                            'error' : "You does not own any device, please create a new one"
                        })

class ListYeucaubaotrixe(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, *args, **kwargs): 
        # equitment_id = request.data.get('equitment')
        equitment_id = kwargs.get('equitment')
        # user = request.user 
        # try:
            # device = user.user_device
        # if device:
            
        result = danhsachyeucaubaotrixe(equitment_id)
        return Response(result)
        # except Exception as ex:
        #     print(ex)
        #     return Response({
        #                     'status': False, 
        #                     'error' : "You does not own any device, please create a new one"
        #                 })

class TaoghichuBaotri(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def post(self, request, *args, **kwargs): 
        equitment = kwargs.get('equitment')
        note = request.data.get('note')
        # user = request.user 
        try:
            # device = user.user_device
        # if device:
            body = request.data
            result = capnhatghichubaotri(equitment, note, body)
            return Response(result)
        except Exception as ex:
            print(ex)
            return Response({
                            'status': False, 
                            'error' : ex.message
                        })



class Danhsachcactinh(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, *args, **kwargs): 
        
        # user = request.user 
        try:
            # device = user.user_device
        # if device:
            
            result = danhsachcactinh()
            return Response(result)
        except Exception as ex:
            # print(ex)
            return Response({
                            'status': False, 
                            'error' : ex.message
                        })


class ListHuyentheotinh(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, *args, **kwargs): 
        province_id = kwargs.get('province')
        user = request.user 
        try:
            device = user.user_device
        # if device:
            
            result = danhsachcachuyentheotinh(province_id)
            return Response(result)
        except Exception as ex:
            print(ex)
            return Response({
                            'status': False, 
                            'error' : "You does not own any device, please create a new one"
                        })

class ListPhuongtheohuyen(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, *args, **kwargs): 
        district_id = kwargs.get('district')
        user = request.user 
        try:
            # device = user.user_device
        # if device:
            
            result = danhsachcacphuongtheohuyen(district_id)
            return JsonResponse(result)
        except Exception as ex:
            print(ex)
            return Response({
                            'status': False, 
                            'error' : "You does not own any device, please create a new one"
                        })


class TatcaDiadiem(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, *args, **kwargs): 
        
        # user = request.user 
        try:
            # device = user.user_device
        # if device:
            
            result = tatcadiadiem()
            return Response(result)
        except Exception as ex:
            # print(ex)
            return Response({
                            'status': False, 
                            'error' : ex.message
                        })

class Taohanhtrinh(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def post(self, request, *args, **kwargs): 
        # equitment = kwargs.get('equitment')
        user = request.user 
        print(user)
        is_superuser = user.is_superuser
        # admin_boad = AdminBoard.objects.filter(user=user).first()
        # if not is_superuser and  not admin_boad :
        #     return HttpResponseRedirect('/auth')
        # if is_superuser or admin_boad.is_vantaihahai_admin :
        user_devices = Device.objects.filter(user = user)
        hahai_member = None
        xe_phutrach = None
        if  len(user_devices)>0:
            print('ha hai member: ', hahai_member)
            user_device = user_devices[0]
            memberships = VantaihahaiMembership.objects.filter(device = user_device)

            if len(memberships)>0:
                membership = memberships[0]
                hahai_member = membership.member
            print("tim kiem xe cua member_id: ",hahai_member.member_id)
            xe_phutrachs = VantaihahaiEquipment.objects.filter(owner_user_id= hahai_member.member_id)
            if len(xe_phutrachs)>0:
                xe_phutrach = xe_phutrachs[0]

        startlocation_id = request.data.get('location_id'),
        endlocation_id = request.data.get('location_dest_id'),
        print(f'start , end: {startlocation_id[0]} - {endlocation_id[0]}' )
        try:
            startlocation_object = VantaiLocation.objects.get(location_id=startlocation_id[0])
            endlocation_object = VantaiLocation.objects.get(location_id=endlocation_id[0])
        except VantaiLocation.DoesNotExist:
            startlocation_object = None
            endlocation_object = None
        
        schedule_date = request.data.get('schedule_date')
        print('schedule_date: ',schedule_date)
        # schedule_date = request.POST['start_date']
        # schedule_time = request.data.get('start_time')
        # schedule_time = request.POST['start_time']
        # product = request.data.get('product')
        # print('product: ', product)

        # start_date_str = schedule_date.strftime('%Y-%m-%d')
        # start_time_string = schedule_time.strftime('%H:%M:%S')
        
        # end_date_str = schedule_date.strftime('%Y-%m-%d')
        # end_time_string = schedule_time.strftime('%H:%M:%S')
        # try:
            # device = user.user_device

            # xe_phutrachs = VantaihahaiEquipment.objects.filter(owner_user_id= hahai_member.member_id)
            # if device:
        body = {

                # "equipment_id": request.data.get('equipment_id'),
                "schedule_date": request.data.get('schedule_date'),
                "location_id": request.data.get('location_id'),
                "location_dest_id": request.data.get('location_dest_id'),
                "equipment_id":xe_phutrach.hahai_id,
                "fleet_product_id": request.data.get('fleet_product_id'),
                "employee_id":hahai_member.employee_id,
            }
        print('body: ',body)
        result = themmoichuyendi(body)
        return Response(result)
        # except Exception as ex:
        #     print(ex)
        #     return Response({
        #                     'status': False, 
        #                     'error' : ex.message
        #                 })