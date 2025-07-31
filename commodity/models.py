from django.conf import settings
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField
from operator import mod
from unittest.util import _MAX_LENGTH
from django.db import models
from auth_user.models import User
from consortium.models import CMI
# Create your models here.


class Commodity(models.Model):
    com_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    cmi_name = models.ForeignKey(CMI, related_name="commodities",verbose_name = "CMI", on_delete=models.CASCADE)
    detail = models.TextField(null=True, blank=True,)
    img = models.ImageField(upload_to='com_img/')
    produced_by = models.TextField(null=True, blank=True,)
    geolat = models.FloatField(null=True, blank=True,)
    geolong = models.FloatField(null=True, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def snippet(self):
        return self.detail[:120] + '...'


    class Meta:
        db_table = "commodity"

auditlog.register(Commodity)

class IecMaterial(models.Model):
    iec_id = models.AutoField(primary_key=True)
    iec_type = models.CharField(max_length=100, null=True, blank=True,)
    title = models.CharField(max_length=255)
    commodity = models.ForeignKey(Commodity, null=True, blank=True, related_name='iecmaterials', on_delete=models.CASCADE)
    target_audience = models.CharField(max_length=100, null=True, blank=True,)
    designed_by = models.CharField(max_length=100, null=True, blank=True,)
    content_by = models.CharField(max_length=100, null=True, blank=True,)
    date_published = models.DateField(blank=True, null=True)
    ip = models.CharField(max_length=30,null=True, blank=True,)
    iec_file = models.FileField(upload_to='iec_files/', blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "iecmaterial"


auditlog.register(IecMaterial)
