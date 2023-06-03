# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.devices.models import Device
from apps.vantai.models import AttackmentHanhTrinh, Hanhtrinh, VantaihahaiMembership
from apps.vantai.unity import cacchuyendihomnaycuataixe, tatcachuyendicuataixe

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
