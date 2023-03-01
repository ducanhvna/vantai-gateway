from django.contrib import admin
from .models import VantaihahaiMember, VantaihahaiMembership, AttackmentHanhTrinh, MemberSalary
# Register your models here.
admin.site.register(VantaihahaiMember)
class VantaihahaiMembershipAdmin(admin.ModelAdmin):
    list_display = ('device','member')
admin.site.register(VantaihahaiMembership,VantaihahaiMembershipAdmin)
admin.site.register(AttackmentHanhTrinh)
admin.site.register(MemberSalary)