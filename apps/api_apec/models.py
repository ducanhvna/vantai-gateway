from django.db import models

class HrmCompany(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    is_ho = models.BooleanField(default=False)
    mis_id = models.CharField(max_length=200, null=False, blank=False)

class CalendarHoliday(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    company = models.ForeignKey(HrmCompany, on_delete=models.CASCADE)
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)
    resource_id = models.CharField(null=True, blank=True)
    time_type = models.CharField(max_length=200, null=True, blank=True)
    
    # 'company_id', 'calendar_id', 'date_from', 'date_to', 'resource_id', 'time_type']
    
# Create your models here.
class HrmShift(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    