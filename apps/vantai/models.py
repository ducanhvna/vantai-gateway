from django.db import models

# Create your models here.

# class Hanhtrinh(models.Model):
#     name = models.CharField(max_length=50)
#     emp_image = models.ImageField(upload_to='images/')

from django.db import models
from apps.devices.models import Device
from django.conf import settings
# Create your models here.
class VantaihahaiMember(models.Model):
    member_id = models.IntegerField(unique=True)
    name = models.TextField()
    employee_id = models.IntegerField(default=0)
    mobile_phone = models.TextField(null=True, blank=True)
    updated_time = models.DateTimeField(null=True,blank=True)

    def __str__(self) -> str:
        return self.name

class MemberSalary(models.Model):
    member = models.ForeignKey(VantaihahaiMember, on_delete=models.CASCADE)
    date = models.DateTimeField("Thoi gian")
    salary = models.DecimalField(max_digits=12, decimal_places=1)
    def __str__(self) -> str:
        return f'{self.member}-{self.date}'

class VantaihahaiMembership(models.Model):
    device = models.ForeignKey(Device, on_delete= models.CASCADE, related_name='device_membership', null=True)
    member = models.OneToOneField(VantaihahaiMember, on_delete=models.CASCADE)
    is_actived = models.BooleanField(default=True)

    def __str__(self) -> str:
        if self.device:
            return f'{self.device.name}-{self.member.name}'
        else:
            return self.member.name


class Hanhtrinh(models.Model):
    hanhtrinh_id = models.IntegerField(null=True)
    location_name = models.TextField(null=True)
    location_dest_name = models.TextField(null=True)
    equipment_id = models.IntegerField(null=True)
    name = models.CharField(max_length=50)
    schedule_date = models.DateTimeField(null=True)
    location_id = models.IntegerField()
    location_dest_id = models.IntegerField()
    location_name = models.TextField(null=True, blank=True)
    location_dest_name= models.TextField(null=True, blank = True)
    ward_id = models.IntegerField()
    ward_dest_id = models.IntegerField()
    district_id = models.IntegerField()
    district_dest_id = models.IntegerField(default=0)
    state_id = models.IntegerField()
    state_dest_id = models.IntegerField()

    emp_image = models.ImageField(upload_to='images/')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='hanhtrinh_created', null=True)
    def __str__(self) -> str:
        return f"{self.location_name} - {self.location_dest_name}"

class AttackmentHanhTrinh(models.Model):
    hanhtrinh= models.ForeignKey(Hanhtrinh, on_delete=models.CASCADE, related_name='hanhtrinh_attackments')
    url = models.TextField()

class VantaiLocation(models.Model):
    name = models.TextField()
    location_id = models.IntegerField()
    ward_id = models.IntegerField()
    ward_name = models.TextField()
    district_id = models.IntegerField()
    district_name = models.TextField()
    state_id = models.IntegerField()
    state_name = models.TextField()
    def __str__(self) -> str:
        return self.name