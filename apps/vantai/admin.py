from django.contrib import admin
from .models import VantaihahaiMember, VantaihahaiMembership, AttackmentHanhTrinh, MemberSalary, VantaihahaiEquipment, \
    VantaiLocation, VantaiProduct, Hanhtrinh
# Register your models here.
admin.site.register(VantaihahaiMember)
class VantaihahaiMembershipAdmin(admin.ModelAdmin):
    list_display = ('device','member')
admin.site.register(VantaihahaiMembership,VantaihahaiMembershipAdmin)
admin.site.register(AttackmentHanhTrinh)
admin.site.register(MemberSalary)
admin.site.register(VantaihahaiEquipment)
admin.site.register(VantaiLocation)
admin.site.register(VantaiProduct)
admin.site.register(Hanhtrinh)