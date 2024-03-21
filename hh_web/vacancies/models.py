from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Vacancy(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    salary = models.JSONField(null=True, blank=True)
    url = models.URLField()
    skills = models.JSONField()
    experience = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=200, null=True, blank=True)
    work_schedule = models.CharField(max_length=200, null=True, blank=True)

class Region(MPTTModel):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']


