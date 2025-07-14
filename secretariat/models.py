from django.conf import settings
from auditlog.registry import auditlog
from operator import mod
from unittest.util import _MAX_LENGTH
from consortium.models import CMI, Consortium
from django.db import models
from auth_user.models import User


# Create your models here.


class Secretariat(models.Model):
    FEMALE = 'Female'
    MALE = 'Male'

    CHOICE_SEX = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )
    DOST = 'DOST-PCAARD'
    CONSORTIUM = 'Consortium'

    CHOICE_ORG = (
        (DOST ,'DOST-PCAARD' ),
        (CONSORTIUM ,'Consortium'),
    )

    secretariat_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100)
    manager = models.ForeignKey('self', related_name='subordinates', on_delete=models.CASCADE, blank=True, null=True)
    consortium_id = models.ForeignKey(Consortium, related_name='+', on_delete=models.CASCADE)
    email_add = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    date_appointed = models.DateField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10, choices=CHOICE_SEX, default=FEMALE)
    organization = models.CharField(max_length=11, choices=CHOICE_ORG, default=CONSORTIUM)
    bach_deg = models.CharField(max_length=100, blank=True, null=True)
    bdyearcompleted = models.IntegerField(blank=True, null=True)
    mas_deg = models.CharField(max_length=100, blank=True, null=True)
    mdyearcompleted = models.IntegerField(blank=True, null=True)
    doc_deg = models.CharField(max_length=100, blank=True, null=True)
    ddyearcompleted = models.IntegerField(blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='secretariat_photo/', blank=True, null=True)
    pds_file = models.FileField(upload_to='secretariat_pds/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return (self.lname) +", "+ (self.fname)
    

    class Meta:
        db_table = "secretariat"

auditlog.register(Secretariat)

