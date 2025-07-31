from django.conf import settings
from auditlog.registry import auditlog
from operator import mod
from unittest.util import _MAX_LENGTH
from django.db import models
from consortium.models import CMI
from auth_user.models import User

# Create your models here.

class Team(models.Model):
    FEMALE = 'Female'
    MALE = 'Male'

    CHOICE_SEX = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )
    RRDCC = 'Regional Research and Development Coordinating Committee'
    R_DC = 'Research and Development Cluster'
    TTC = 'Technology Transfer Cluster'
    SCC = 'Science Communication Cluster'
    ICTC = 'Information and Communications Technology Cluster'

    CHOICE_TEAM= (
        (RRDCC, 'RRDCC'),
        (R_DC, 'R&DC'),
        (TTC, 'TTC'),
        (SCC, 'SCC'),
        (ICTC, 'ICTC'),
    )
    member_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100)
    cmi = models.ForeignKey(CMI, related_name='team', verbose_name = "CMI", on_delete=models.CASCADE)
    teams = models.CharField(max_length=60)  # Remove CHOICE_TEAM
    email_add = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    date_appointed = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10, choices=CHOICE_SEX, default=FEMALE) 
    specialization = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='team_photo/', blank=True, null=True)
    pds_file = models.FileField(upload_to='pds_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return (self.lname) +", "+ (self.fname)
    
    class Meta:
        db_table = 'team'

auditlog.register(Team)