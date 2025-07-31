from django.conf import settings
from auditlog.registry import auditlog
from operator import mod
from unittest.util import _MAX_LENGTH
from django.db import models
from auth_user.models import User

# Create your models here.
class Consortium(models.Model):
    consortium_id = models.AutoField(primary_key=True)
    consortium_code = models.CharField(max_length=50)
    consortium_name = models.CharField(max_length=255)
    consortium_address = models.CharField(max_length=255)
    geolat = models.FloatField(blank=True, null=True)
    geolong = models.FloatField(blank=True, null=True)
    consortium_logo = models.ImageField(upload_to='consortium_logos/')
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    consortium_desc = models.TextField(blank=True, null=True)
    consortium_objectives = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=255, blank=True, null=True)
    fb_url = models.URLField(max_length=255, blank=True, null=True)
    yt_url = models.URLField(max_length=255, blank=True, null=True)
    telno = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.consortium_code
    
    def snippet(self):
        return self.consortium_desc[:120] + '...'

    def snippetname (self):
        return self.consortium_name[:27] + '...'

    class Meta:
        db_table = "consortium"

auditlog.register(Consortium)


class CMI(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'

    CHOICE_STATUS = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )
    agency_id = models.AutoField(primary_key=True)
    agency_code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    is_cmi= models.BooleanField(default=True)
    consortium_id = models.ForeignKey(Consortium, related_name="+", on_delete=models.CASCADE)
    # consortium_acronym = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    geolat = models.FloatField(blank=True, null=True)
    geolong = models.FloatField(blank=True, null=True)
    logo = models.ImageField(upload_to='cmi_logos/')
    # mission = models.TextField(blank=True, null=True)
    # vision = models.TextField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    # consortium_objectives = models.TextField(blank=True, null=True)
    # fb_url = models.URLField(max_length=255, blank=True, null=True)
    # yt_url = models.URLField(max_length=255, blank=True, null=True)
    contact_no = models.CharField(max_length=70, blank=True, null=True)
    telno = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100, choices=CHOICE_STATUS, default=ACTIVE)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.agency_code
    
    def snippet(self):
        return self.detail[:120] + '...'

    def snippetname (self):
        return self.name[:27] + '...'

    class Meta:
        db_table = "cmi"

auditlog.register(CMI)
