from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import HanhtrinhForm
from .models import AttackmentHanhTrinh, MemberSalary, VantaihahaiMember,VantaihahaiMembership
from django.views.generic import DetailView
from .models import Hanhtrinh

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
