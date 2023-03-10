from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.crypto import get_random_string
# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
# import generic UpdateView
from django.views.generic.edit import UpdateView
import string
from .forms import HanhtrinhForm, HahaiMembershipForm, AttackmentForm, KmHanhtrinhForm
from apps.authentication.forms import SignUpForm
from .models import AttackmentHanhTrinh, MemberSalary, VantaiLocation, VantaiProduct, VantaihahaiEquipment, VantaihahaiMember,VantaihahaiMembership
from django.views.generic import DetailView, ListView
from .models import Hanhtrinh, Device, VantaihahaiMember
from .unity import GetThongtintaixe, danhsachtatcaxe, tatcachuyendicuataixe, cacchuyendihomnaycuataixe, tatcadiadiem, themmoichuyendi, \
    capnhatsokmketthuchanhtrinh, capnhatsokmbatdauhanhtrinh
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from apps.devices.models import Device
import datetime

class HanhtrinhImage(TemplateView):

    form = KmHanhtrinhForm
    template_name = 'vantai/emp_image.html'

    def post(self, request, *args, **kwargs):

        form = AttackmentForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('emp_image_display', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)     
    def get_context_data(self, **kwargs):
        context = super(HanhtrinhImage, self).get_context_data(**kwargs)

        form = KmHanhtrinhForm(initial={'odo':1000,'hanhtrinh': Hanhtrinh.objects.get(hanhtrinh_id=7321)})  # instance= None

        context["form"] = form
        #context["latest_article"] = latest_article

        return context
    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)

class EmpImageDisplay(DetailView):
    model = AttackmentHanhTrinh
    template_name = 'vantai/emp_image_display.html'
    context_object_name = 'emp'

def vantaihahai_view(request):
    user = request.user
    print(user)
    is_superuser = user.is_superuser
    # admin_boad = AdminBoard.objects.filter(user=user).first()
    # if not is_superuser and  not admin_boad :
    #     return HttpResponseRedirect('/auth')
    # if is_superuser or admin_boad.is_vantaihahai_admin :
    if is_superuser:
        members = list(VantaihahaiMember.objects.all().values('name','member_id'))
        member_ship = list(VantaihahaiMembership.objects.select_related().all().order_by('-member'))
        dic = {}

        # for mem in member_ship:
        #     if mem['member__name'] not in dic :
        #         dic[mem['member__name']] = [{'id_mbs':mem['id'],'id':mem['device__id'],'type':mem['device__type']}]
        #     else :
        #         dic[mem['member__name']].append({'id_mbs':mem['id'],'id':mem['device__id'],'type':mem['device__type']})
        # lis_membership = []
        # for key,val in dic.items():
        #     dic_1 = {
        #         "name":key,
        #         "count_device":len(val),
        #         "devices":{
        #             "first_device":val[0],
        #             "device":val[1:] if len(val) > 1 else []
        #         }
        #     }
        #     lis_membership.append(dic_1)
        context = {'members': members,'memberships': member_ship}
        return render(request, 'vantai/vantaihahai.html', context)
    else:
        return HttpResponseRedirect('/auth')
    

class HahaiMemberListView(LoginRequiredMixin, ListView):
    model = VantaihahaiMember
    context_object_name = "members"
    template_name = "vantai/danhsachmember.html"
    def get_queryset(self):
        # queryset = self.model.objects.all().select_related("account")
        # queryset = super(PodDetailView, self).get_queryset()
        print('abc',self.request.user)
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
        queryset= self.model.objects.select_related().all()
        print(queryset)
        return queryset
# DiadiemListView
class DiadiemListView(LoginRequiredMixin, ListView):
    model = Hanhtrinh
    context_object_name = "joyneys"
    template_name = "vantai/tatcadiadiem.html"
    def get_queryset(self):
        # queryset = self.model.objects.all().select_related("account")
        # queryset = super(PodDetailView, self).get_queryset()
        print('abc',self.request.user)
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
        queryset= tatcadiadiem()['data']['results']
        print(queryset)
        return queryset
# MathangListView
class MathangListView(LoginRequiredMixin, ListView):
    model = VantaiProduct
    context_object_name = "joyneys"
    template_name = "vantai/tatcamathang.html"
    def get_queryset(self):
        # queryset = self.model.objects.all().select_related("account")
        # queryset = super(PodDetailView, self).get_queryset()
        print('abc',self.request.user)
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
        queryset= VantaiProduct.objects.all()
        print(queryset)
        return queryset

# EquimentListView
class EquipmentListView(LoginRequiredMixin, ListView):
    model = Hanhtrinh
    context_object_name = "joyneys"
    template_name = "vantai/equipmentlist.html"
    def get_queryset(self):
        # queryset = self.model.objects.all().select_related("account")
        # queryset = super(PodDetailView, self).get_queryset()
        print('abc',self.request.user)
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
        queryset= danhsachtatcaxe()['data']['results']
        print(queryset)
        for item in queryset:
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
        
        return queryset
    

class ChuyendiListView(LoginRequiredMixin, ListView):
    model = Hanhtrinh
    context_object_name = "joyneys"
    template_name = "vantai/tatcachuyendi.html"
    def get_queryset(self):
        # queryset = self.model.objects.all().select_related("account")
        # queryset = super(PodDetailView, self).get_queryset()
        print('abc',self.request.user)
        queryset = []
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
                queryset= tatcachuyendicuataixe(employee_id)['data']['results']
                print(queryset)
                results= []
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
                            hanhtrinh.schedule_date = datetime.datetime.strptime(item['schedule_date'], "%Y-%m-%d")
                            hanhtrinh.location_name = item['location_name']
                            hanhtrinh.location_dest_name = item['location_dest_name']
                            hanhtrinh.odo_start = item['odometer_start']
                            hanhtrinh.odo_end = item['odometer_dest']
                            if item['ward_id']:
                                hanhtrinh.ward_id  = item['ward_id']
                            hanhtrinh.save()
                            
                    except Exception as ex:
                        print('sync chuyen di err: ', ex)
        # else:        
            queryset= Hanhtrinh.objects.filter(employee_id = employee_id).order_by('-schedule_date', '-created_time')
        print(queryset)
        return queryset

class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    context_object_name = "devices"
    template_name = "vantai/listdevices.html"
    def get_queryset(self):
        # queryset = self.model.objects.all().select_related("account")
        # queryset = super(PodDetailView, self).get_queryset()
        print('abc',self.request.user)
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
        queryset= self.model.objects.all()
        print(queryset)
        return queryset

def tatcachuyendicuataixe_view(request):
    user = request.user
    print(user)
    is_superuser = user.is_superuser
    # admin_boad = AdminBoard.objects.filter(user=user).first()
    # if not is_superuser and  not admin_boad :
    #     return HttpResponseRedirect('/auth')
    # if is_superuser or admin_boad.is_vantaihahai_admin :
    if is_superuser:
        members = list(VantaihahaiMember.objects.all().values('name','member_id'))
        member_ship = list(VantaihahaiMembership.objects.select_related().all().order_by('-member'))
        dic = {}

        # for mem in member_ship:
        #     if mem['member__name'] not in dic :
        #         dic[mem['member__name']] = [{'id_mbs':mem['id'],'id':mem['device__id'],'type':mem['device__type']}]
        #     else :
        #         dic[mem['member__name']].append({'id_mbs':mem['id'],'id':mem['device__id'],'type':mem['device__type']})
        # lis_membership = []
        # for key,val in dic.items():
        #     dic_1 = {
        #         "name":key,
        #         "count_device":len(val),
        #         "devices":{
        #             "first_device":val[0],
        #             "device":val[1:] if len(val) > 1 else []
        #         }
        #     }
        #     lis_membership.append(dic_1)
        context = {'members': members,'memberships': member_ship}
        return render(request, 'vantai/vantaihahai.html', context)
    else:
        return HttpResponseRedirect('/auth')

class EditMemberShipView(UpdateView):
    model = VantaihahaiMembership
    form_class = HahaiMembershipForm
    template_name = 'vantai/editHahaimbership.html'

    
    def get_context_data(self, **kwargs):
        context = super(EditMemberShipView, self).get_context_data(**kwargs)
        context["members"] = self.get_queryset()
        return context
    def get_object(self):
     
        memberships = VantaihahaiMembership.objects.filter(member__pk=self.kwargs['pk'])
        if len(memberships) > 0:
            return memberships[0]
        else:
            print("find member: ",self.kwargs['pk'])
            member = VantaihahaiMember.objects.get(pk = self.kwargs['pk'])
            membership_object = VantaihahaiMembership(member=member)
            membership_object.save()
            return membership_object 

    def get_success_url(self):
        pass

class UpdatedanhsachmemberWeb(LoginRequiredMixin, View): 
 
    # authentication_classes = [authentication.SessionAuthentication]
    def get(self, request, *args, **kwargs): 
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa DR aaaaaaaaaaaaaa")
        # equitment = kwargs.get('equitment')
        # note = request.data.get('note')
        # user = request.user 
        try:
            # device = user.user_device
        # if device:
            # body = request.data
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
            return JsonResponse({
                            'status': 'OK', 
                            
                        })
        except Exception as ex:
            print(ex)
            return JsonResponse({
                            'status': False, 
                            'error' : "You does not own any device, please create a new one"
                        })



def register_user(request):
    msg = None
    success = False
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
    else:
        print("khong thay device cho member")
    if request.method == "POST":
        form = HanhtrinhForm(request.POST)
        # if form.is_valid():
        if form.is_valid() or True:
            print('valid form')
            startlocation_id = request.POST['StartLocationId']
            endlocation_id = request.POST['EndLocationId']
            print(f'start , end: {startlocation_id} - {endlocation_id}' )
            try:
                startlocation_object = VantaiLocation.objects.get(location_id=startlocation_id)
                endlocation_object = VantaiLocation.objects.get(location_id=endlocation_id)
            except VantaiLocation.DoesNotExist:
                startlocation_object = None
                endlocation_object = None
            schedule_date = form.cleaned_data['start_date']
            # schedule_date = request.POST['start_date']
            schedule_time = form.cleaned_data['start_time']
            # schedule_time = request.POST['start_time']
            product = form.cleaned_data['product']
            # product = request.POST['product']
            # product = VantaiProduct.objects.get(pk= product)
            print('get product', product.product_id)
            print("hanh trinh bat dau: ", schedule_date)
            print("hanh trinh bat dau: ", schedule_date.year)
            print("hanh trinh bat dau: ", schedule_date.month)
            print("hanh trinh bat dau: ", schedule_date.day)
            print("hanh trinh  bat dau loc: ", schedule_time.hour)
            print("hanh trinh  bat dau loc: ", schedule_time.minute)
            print("hanh trinh  bat dau loc: ", schedule_time.second)

            # form.save()
        
            start_date_str = schedule_date.strftime('%Y-%m-%d')
            start_time_string = schedule_time.strftime('%H:%M:%S')
            
            end_date_str = schedule_date.strftime('%Y-%m-%d')
            end_time_string = schedule_time.strftime('%H:%M:%S')
            print(end_time_string)
            # body = {
            #     "equipment_id":xe_phutrach.hahai_id,
            #     "schedule_date": f"{s_y}-{s_m}-{s_d} {s_h}:{s_minute}:{s_s}",
            #     "location_id": startlocation_id,
            #     # "location_name": startlocation_object.name,

            #     "location_dest_id": endlocation_id,
                
            # }
            body = {
                "equipment_id":xe_phutrach.hahai_id,
                "schedule_date": f"{start_date_str} {start_time_string}",
                "end_date": f"{end_date_str} {end_time_string}",
                "location_id": startlocation_id,
                "location_dest_id": endlocation_id,
                "employee_id":hahai_member.employee_id,
                "fleet_product_id": product.product_id
                # "location_name": "Hà Nội",
                # "location_dest_name": "Sài Gòn"
            }
            print(body)
            abc = themmoichuyendi(body)
            # {'success': True, 'data': 
            # {'id': 7299, 
            #   'equipment_id': {'id': 3, 'name': 'Xe 01', 'license_plate': '001'}, 
            #   'location_name': 'Hà Nội', 
            #   'location_dest_name': 'Sài Gòn', 
            #   'incurred_fee': 0.0, 'incurred_note': None, 
            #   'incurred_fee_2': 0.0, 'incurred_note_2': None, 
            #   'schedule_date': '2023-03-04', 'start_date': None, 
            #   'end_date': None, 'state': '1_draft', 'ward_id': None, 
            #   'district_id': None, 'state_id': None, 'ward_dest_id': None, 'district_dest_id': None, 
            #   'state_dest_id': None, 'company_name': None, 'eating_fee': 0.0, 'law_money': 0.0, 'road_tiket_fee': 0.0, 
            # 'fee_total': 0.0, 'odometer_start': 0, 'odometer_dest': 0, 'attachment_ids': []}, 'errorData': {}}
            print("Kết quả", abc)
            return HttpResponseRedirect('/vantai/tatcachuyendi')
        else:
            msg = 'Form is not valid'
    else:
        form = HanhtrinhForm()
    joyneys = tatcadiadiem()['data']['results']
    # print(joyneys)
    return render(request, "vantai/taohanhtrinh.html", {"form": form, 'member':hahai_member, "xe": xe_phutrach, "joyneys": joyneys, "msg": msg, "success": success})

# Create your models here.
def create_new_ref_number():
    code = get_random_string(8, allowed_chars=string.ascii_uppercase + string.digits)
    return code

def register_user_for_member(request, pk):
    msg = None
    success = False
    member = VantaihahaiMember.objects.get(pk= pk)
    memberships = VantaihahaiMembership.objects.filter(member__id=pk)
    if len(memberships)==0:
        membership = VantaihahaiMembership(member = member)
        membership.save()
    else:
        membership = memberships[0]
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
                    membership.device = device_object
                    membership.save()
            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
        
    return render(request, "vantai/register_for_member.html", {"form": form, "member":member, "msg": msg, "success": success})

 
# Create your views here.
 
 
def hotel_image_view(request):
 
    if request.method == 'POST':
        form = AttackmentForm(request.POST, request.FILES)
 
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = AttackmentForm()
    return render(request, 'vantai/up_image.html', {'form': form})
 
 
def success(request):
    return HttpResponse('successfully uploaded')

def display_hotel_images(request):
 
    if request.method == 'GET':
 
        # getting all the objects of hotel.
        Hotels = AttackmentHanhTrinh.objects.all()
        return render(request, 'vantai/display_image.html',{'hotel_images': Hotels})
    
# CapnhatBatdauHanhtrinh
class CapnhatBatdauHanhtrinhView(TemplateView):
    
    form = KmHanhtrinhForm
    template_name = 'vantai/batdauhanhtrinh.html'

    def post(self, request, *args, **kwargs):
        """ Check post data
        """
        form = KmHanhtrinhForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            hanhtrinh_pk = self.kwargs['pk']
            hanhtrinh = Hanhtrinh.objects.get(pk=hanhtrinh_pk)
            odo_start = form.cleaned_data['odo']

            main_img =form.cleaned_data['main_img']
            print(obj.main_img)
            print(odo_start)
            hanhtrinh.odo_start = odo_start
            hanhtrinh.save()
            body={}
            attackements = None
            if main_img:
                attackements=[main_img]
            capnhatsokmbatdauhanhtrinh(hanhtrinh.hanhtrinh_id, odo_start, body, attackements)
            return HttpResponseRedirect('/vantai/chitiethanhtrinh/{}/'.format(hanhtrinh.id))

        context = self.get_context_data(form=form)
        
        return self.render_to_response(context)     
    def get_context_data(self, **kwargs):
        """Overide get_context_data method
        """
        
        context = super(CapnhatBatdauHanhtrinhView, self).get_context_data(**kwargs)
        hanhtrinh_pk = self.kwargs['pk']
        hanhtrinh = Hanhtrinh.objects.get(pk=hanhtrinh_pk)
        form = KmHanhtrinhForm(initial={'name':f"Start-{hanhtrinh.hanhtrinh_id}",'odo':1000,'hanhtrinh': hanhtrinh})  # instance= None

        context["form"] = form
        #context["latest_article"] = latest_article

        return context
    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)


# CapnhatKetthucHanhtrinh
class CapnhatKetthucHanhtrinhView(TemplateView):
    
    form = KmHanhtrinhForm
    template_name = 'vantai/ketthuchanhtrinh.html'

    def post(self, request, *args, **kwargs):
        """ Check post data
        """
        form = KmHanhtrinhForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            hanhtrinh_pk = self.kwargs['pk']
            hanhtrinh = Hanhtrinh.objects.get(pk=hanhtrinh_pk)
            odo_end = form.cleaned_data['odo']
            main_img = form.cleaned_data['main_img']
            print(obj.main_img)
            print(odo_end)
            hanhtrinh.odo_end = odo_end
            hanhtrinh.save()
            attackements = None
            if main_img:
                attackements=[main_img]
            body={}
            capnhatsokmketthuchanhtrinh(hanhtrinh.hanhtrinh_id, odo_end, body, attackements)
            return HttpResponseRedirect('/vantai/chitiethanhtrinh/{}/'.format(hanhtrinh.id))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)     
    def get_context_data(self, **kwargs):
        """Overide get_context_data method
        """
        
        context = super(CapnhatKetthucHanhtrinhView, self).get_context_data(**kwargs)
        hanhtrinh_pk = self.kwargs['pk']
        hanhtrinh = Hanhtrinh.objects.get(pk=hanhtrinh_pk)
        form = KmHanhtrinhForm(initial={'name':f"End-{hanhtrinh.hanhtrinh_id}",'odo':1000,'hanhtrinh': hanhtrinh})  # instance= None

        context["form"] = form
        #context["latest_article"] = latest_article

        return context
    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)


class ChitiethanhtrinhView(DetailView):
    model = Hanhtrinh
    template_name = 'vantai/emp_image_display.html'
    context_object_name = 'emp'
    def get_context_data(self, **kwargs):
        """Overide get_context_data method
        """
        
        context = super(ChitiethanhtrinhView, self).get_context_data(**kwargs)
        hanhtrinh_pk = self.kwargs['pk']
        # hanhtrinh = Hanhtrinh.objects.get(pk=hanhtrinh_pk)
        # form = KmHanhtrinhForm(initial={'name':f"Start-{hanhtrinh.hanhtrinh_id}",'odo':1000,'hanhtrinh': hanhtrinh})  # instance= None
        attackments = AttackmentHanhTrinh.objects.filter(hanhtrinh__id =hanhtrinh_pk)
        context["attackments"] = attackments
        #context["latest_article"] = latest_article

        return context
