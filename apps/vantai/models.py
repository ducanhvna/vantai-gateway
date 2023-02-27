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
    device = models.OneToOneField(Device, on_delete= models.CASCADE, related_name='device_membership')
    member = models.ForeignKey(VantaihahaiMember, on_delete=models.CASCADE)
    def __str__(self) -> str:
        
        return self.device.name


class Hanhtrinh(models.Model):
    hanhtrinh_id = models.IntegerField(null=True)
    location_name = models.TextField(null=True)
    location_dest_name = models.TextField(null=True)
    equipment_id = models.IntegerField(null=True)
    name = models.CharField(max_length=50)
    emp_image = models.ImageField(upload_to='images/')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='hanhtrinh_created', null=True)
    def __str__(self) -> str:
        return f"{self.location_name} - {self.location_dest_name}"

class AttackmentHanhTrinh(models.Model):
    hanhtrinh= models.ForeignKey(Hanhtrinh, on_delete=models.CASCADE, related_name='hanhtrinh_attackments')
    url = models.TextField()
