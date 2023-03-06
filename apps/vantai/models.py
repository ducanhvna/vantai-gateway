from django.db import models
from django.conf import settings
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
class VantaihahaiEquipment(models.Model):
    hahai_id = models.IntegerField(unique=True)
    owner_user_id = models.IntegerField(default=0)
    owner_user_name = models.TextField()
    name = models.TextField()
    license_plate = models.TextField()

    def __str__(self) -> str:
        return self.name

class MemberSalary(models.Model):
    member = models.ForeignKey(VantaihahaiMember, on_delete=models.CASCADE)
    date = models.DateTimeField("Thoi gian")
    salary = models.DecimalField(max_digits=12, decimal_places=1)
    def __str__(self) -> str:
        return f'{self.member}-{self.date}'

class VantaihahaiMembership(models.Model):
    device = models.OneToOneField(Device, on_delete= models.CASCADE, related_name='device_membership', null=True)
    member = models.OneToOneField(VantaihahaiMember, related_name='member_memberships', on_delete=models.CASCADE)
    is_actived = models.BooleanField(default=True)

    def __str__(self) -> str:
        if self.device:
            return f'{self.device.name}-{self.member.name}'
        else:
            return self.member.name
        
class VantaiProduct(models.Model):
    name = models.TextField()
    product_id = models.IntegerField(default=0, unique=True)
    def __str__(self) -> str:
        return self.name


class Hanhtrinh(models.Model):
    hanhtrinh_id = models.IntegerField(null=True)
    equipment_id = models.IntegerField(null=True)
    name = models.CharField(max_length=50)
    product = models.ForeignKey(VantaiProduct, on_delete=models.CASCADE, null=True, blank=True)
    schedule_date = models.DateTimeField(null=True)
    location_id = models.IntegerField(default=0)
    location_dest_id = models.IntegerField(default=0)
    location_name = models.TextField(null=True, blank=True)
    location_dest_name= models.TextField(null=True, blank = True)
    ward_id = models.IntegerField(default=0)
    ward_dest_id = models.IntegerField(default=0)
    district_id = models.IntegerField(default=0)
    district_dest_id = models.IntegerField(default=0)
    state_id = models.IntegerField(default=0)
    state_dest_id = models.IntegerField(default=0)

    emp_image = models.ImageField(upload_to='images/')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='hanhtrinh_created', null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
   
    def __str__(self) -> str:
        return f"{self.location_name} - {self.location_dest_name}"

class AttackmentHanhTrinh(models.Model):
    hanhtrinh= models.ForeignKey(Hanhtrinh, on_delete=models.CASCADE, related_name='hanhtrinh_attackments')
    url = models.TextField()

class VantaiLocation(models.Model):
    name = models.TextField()
    location_id = models.IntegerField(default=0, unique=True)
    ward_id = models.IntegerField(default=0)
    ward_name = models.TextField(null=True,blank=True)
    district_id = models.IntegerField(default=0)
    district_name = models.TextField(null=True,blank=True)
    state_id = models.IntegerField(default=0)
    state_name = models.TextField(null=True,blank=True)
    def __str__(self) -> str:
        return self.name
    
