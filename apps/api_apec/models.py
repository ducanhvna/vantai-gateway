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
    start_work_time = models.TimeField(null=False, blank=False)
    end_work_time = models.TimeField(null=False, blank=False)
    total_work_time = models.IntegerField(null=False, blank=False)
    start_rest_time = models.TimeField(null=False, blank=False)
    end_rest_time = models.TimeField(null=False, blank=False)
    company = models.ForeignKey(HrmCompany, on_delete=models.CASCADE)
    rest_shifts = models.BooleanField(default=False)
    fix_rest_time = models.BooleanField(default=False)
    night = models.BooleanField(default=False)
    night_eat = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    breakfast = models.BooleanField(default=False)
    efficiency_factor = models.DecimalField(decimal_places=2, max_digits=5)