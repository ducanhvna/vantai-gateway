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
from .forms import HanhtrinhForm, HahaiMembershipForm
from apps.authentication.forms import SignUpForm
from .models import AttackmentHanhTrinh, MemberSalary, VantaihahaiMember,VantaihahaiMembership
from django.views.generic import DetailView, ListView
from .models import Hanhtrinh, Device, VantaihahaiMember
from .unity import GetThongtintaixe, tatcachuyendicuataixe, cacchuyendihomnaycuataixe, tatcadiadiem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone


class HanhtrinhImage(TemplateView):

    form = HanhtrinhForm
    template_name = 'vantai/emp_image.html'

    def post(self, request, *args, **kwargs):

        form = HanhtrinhForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('emp_image_display', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class EmpImageDisplay(DetailView):
    model = Hanhtrinh
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
        queryset= self.model.objects.all()
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

class ChuyendiListView(LoginRequiredMixin, ListView):
    model = Hanhtrinh
    context_object_name = "joyneys"
    template_name = "vantai/tatcachuyendi.html"
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
        queryset= tatcachuyendicuataixe(4)['data']['results']
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
                if taixe:
                    try:
                        print(f" member {i} existed")
                        member = VantaihahaiMember.objects.get(member_id=i)
                        member.name = taixe['data']['name']
                        member.employee_id = taixe['data']['employee_id']['id']
                        member.mobile_phone = taixe['data']['employee_id']['mobile_phone']
                        member.save()
                    except VantaihahaiMember.DoesNotExist:
                        print("Create new member", taixe)
                        member = VantaihahaiMember(member_id = i, name = taixe['data']['name'],
                                                employee_id = taixe['data']['employee_id']['id'],
                                                mobile_phone = taixe['data']['employee_id']['mobile_phone'],
                                                updated_time = timezone.now())
                        member.save()
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
    if  len(user_devices)>0:
        print('ha hai member: ', hahai_member)
        user_device = user_devices[0]
        memberships = VantaihahaiMembership.objects.filter(device = user_device)

        if len(memberships)>0:
            membership = memberships[0]
            hahai_member = membership.member
    else:
        print("khong thay device cho member")
    if request.method == "POST":
        # form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get("username")
            # raw_password = form.cleaned_data.get("password1")
            # user = authenticate(username=username, password=raw_password)

            # msg = 'User created successfully.'
            # success = True
            # device = request.POST.get("device")
            # print("device cua chung ta", username)

            # print("device cua chung ta", device)
            # if user is not None:
            #     if device != None and device != '':
            #     # Create new device
            #         device_type = 3
            #         if device == 'IOS':
            #             device_type = 2
            #         elif device == 'ANDROID':
            #             device_type = 1
                    
            #         device_id = device + create_new_ref_number()
            #         while len(Device.objects.filter(id= device_id))>0:
            #             device_id = device + create_new_ref_number()
            #         device_object = Device(type = device_type, user = user, id =device_id)
            #         device_object.save()

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = HanhtrinhForm()
    joyneys = tatcadiadiem()['data']['results']
    return render(request, "vantai/taohanhtrinh.html", {"form": form, 'member':hahai_member, "joyneys": joyneys, "msg": msg, "success": success})

# Create your models here.
def create_new_ref_number():
    code = get_random_string(8, allowed_chars=string.ascii_uppercase + string.digits)
    return code

def register_user_for_member(request, pk):
    msg = None
    success = False
    membership = VantaihahaiMembership.objects.get(pk= pk)
    member = membership.member
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
