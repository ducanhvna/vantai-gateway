from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.db.models.aggregates import Count
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string
import string

# Create your models here.
def create_new_ref_number():
    code = get_random_string(8, allowed_chars=string.ascii_uppercase + string.digits)
    return code
class Device(models.Model):
    ANDROID = 1
    IPHONE = 2
    CHROME = 3
    OTHER = 4
    # referral = models.ForeignKey('Device',null=True,blank=True,on_delete=models.SET_NULL, related_name='childs')
    DEVICE_CHOICES = ( (ANDROID, 'Android'), (IPHONE, 'iPhone') , (CHROME,'Chrome'), (OTHER,'Others'))
    type = models.SmallIntegerField(choices = DEVICE_CHOICES, default=OTHER)
    user   = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                    on_delete=models.CASCADE,
                                    primary_key=True, related_name='user_device')
    id = models.TextField(unique=True)
   
    default_shipping_address_id = models.IntegerField(null=True, blank=True)
    name   = models.CharField(max_length=8,
                null=False, blank=False, 
                unique=True,
                default=create_new_ref_number)
    device_firebase_address = models.CharField(max_length=255,
                null=True, 
                unique=True)

    def __str__(self) -> str:
        return self.name
   