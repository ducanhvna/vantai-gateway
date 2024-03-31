from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=512)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    dbname = models.CharField(max_length=200)
    api_version = models.CharField(max_length=200, blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)

    # users = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL,
    #     related_name='groups',
    #     through='Participation'
    # )
    def __str__(self):
        return self.name

# class Participation(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     username = models.CharField(max_length=200, null=True, blank=True)
#     password = models.CharField(max_length=200, null=True, blank=True)
#     def __str__(self):
#         return self.name