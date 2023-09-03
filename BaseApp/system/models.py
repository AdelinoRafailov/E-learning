from distutils.command.upload import upload
from sys import maxsize
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class AppDetails(models.Model):
    name = models.CharField(max_length=30, blank=True)
    logo = models.ImageField(upload_to="static/system")
    created_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def AppDetails_Save(name, logo, created_by):
        try:
            AppDetails(name=name, logo=logo, created_by=created_by).save()
            return True
        except Exception as e:
            return False

    def AppDetails_Get():
        return AppDetails.objects.last()

