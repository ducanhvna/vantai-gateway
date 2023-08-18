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
    GetThongtintaixe, danhsachtatcaxe, VanTaiHaHai, thongtinxe, danhsachyeucaubaotrixe, capnhatghichubaotri, \
    danhsachcacphuongtheohuyen, danhsachcachuyentheotinh, danhsachcactinh, tatcadiadiem
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

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
                print(queryset)
                lst_htrinh = [item['id'] for item in queryset['data']['results']]
                Hanhtrinh.objects.filter(~Q(hanhtrinh_id__in = lst_htrinh)).delete()
                for item in queryset['data']['results']:
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
        # attackements = request.data.get('attackements')
        attackements = []
        ht_object = Hanhtrinh.objects.get(hanhtrinh_id=hanhtrinh)
        ht_object.odo_end= km_end
        ht_object.save()
        vantai = VanTaiHaHai()
        vantai.capnhatsokmketthuchanhtrinh(ht_object.hanhtrinh_id, km_end, None, attackements)
            # attachments = body['attachments']
            # for item in attachments:
            #     atts= AttackmentHanhTrinh.objects.filter(hanhtrinh = ht_object, url=item)
            #     if len(atts) == 0:
            #         att = AttackmentHanhTrinh(hanhtrinh = ht_object, url= item)
            #         att.save()

        result = chitiethanhtrinh(ht_object.hanhtrinh_id)
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

class CapnhatkmBatdau(APIView): 
    permission_classes = (IsAuthenticated,)
    # authentication_classes = [authentication.SessionAuthentication]
    def put(self, request, *args, **kwargs): 
        hanhtrinh = kwargs.get('hanhtrinh')
        km_end = request.data.get('km')
        # attackements = request.data.get('attackements')
        attackements = []
        ht_object = Hanhtrinh.objects.get(hanhtrinh_id=hanhtrinh)
        ht_object.odo_start= km_end
        ht_object.save()
        vantai = VanTaiHaHai()
        vantai.capnhatsokmbatdauhanhtrinh(ht_object.hanhtrinh_id, km_end, None, attackements)
            # attachments = body['attachments']
            # for item in attachments:
            #     atts= AttackmentHanhTrinh.objects.filter(hanhtrinh = ht_object, url=item)
            #     if len(atts) == 0:
            #         att = AttackmentHanhTrinh(hanhtrinh = ht_object, url= item)
            #         att.save()
        result = chitiethanhtrinh(ht_object.hanhtrinh_id)
        # result['data']['sid'] = result['data']['id']
        # result['data']['id'] = ht_object.pk
        return Response(result)

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
        note = request.data.get('note')
        # user = request.user 
        try:
            # device = user.user_device

            # xe_phutrachs = VantaihahaiEquipment.objects.filter(owner_user_id= hahai_member.member_id)
            # if device:
            body = {
                    "equipment_id": request.data.get('equipment_id'),
                    "schedule_date": request.data.get('schedule_date'),
                    "location_id": request.data.get('location_id'),
                    "location_dest_id": request.data.get('location_dest_id'),
                    "employee_id":request.data.get('employee_id'),
                    "fleet_product_id": request.data.get('fleet_product_id')
                }
            result = themmoichuyendi(body)
            return Response(result)
        except Exception as ex:
            print(ex)
            return Response({
                            'status': False, 
                            'error' : ex.message
                        })