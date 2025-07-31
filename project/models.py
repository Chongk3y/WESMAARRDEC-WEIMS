from django.conf import settings
from simple_history.models import HistoricalRecords
from auditlog.registry import auditlog
from operator import mod
from unittest.util import _MAX_LENGTH
from django.db import models
from auth_user.models import User
from commodity.models import Commodity, IecMaterial
from program.models import Program, Researcher, Stakeholder
from consortium.models import CMI


# Create your models here.


class Sdg(models.Model):
    sdg_no = models.AutoField(primary_key=True)
    sdg_title = models.CharField(max_length=100)
    sdg_desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.sdg_title

    class Meta:
        db_table = "sdg"

    def snippet(self):
        return self.sdg_desc[:90] + '...'

auditlog.register(Sdg)

class PriorityArea(models.Model):
    priority_id = models.AutoField(primary_key=True)
    area = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.area

    class Meta:
        db_table = "priority_area"

auditlog.register(PriorityArea)


class Project(models.Model):
    ONGOING = 'Ongoing'
    COMPLETED = 'Completed'

    CHOICE_STATUS = (
        (ONGOING, 'Ongoing'),
        (COMPLETED, 'Completed'),
    )

    R_AND_D = 'R&D'
    NON_R_AND_D = 'Non-R&D'

    CHOICE_TYPE = (
        (R_AND_D, 'R&D'),
        (NON_R_AND_D, 'Non-R&D'),
    )
    proj_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    prog_id= models.ForeignKey(Program, null=True, blank=True, related_name='proj_prog', on_delete=models.CASCADE)
    proj_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=CHOICE_STATUS, default=ONGOING)
    proj_type = models.CharField(max_length=20, choices=CHOICE_TYPE, default=R_AND_D, verbose_name = "Project Type")
    #proj_type_sub = models.CharField(max_length=20)
    commodity = models.ManyToManyField(Commodity, blank=True, related_name="proj_com", verbose_name="Commodity")
    proj_leader = models.ForeignKey(Researcher, related_name='proj_leader', on_delete=models.CASCADE, verbose_name = "Project Leader")
    priority = models.ForeignKey(PriorityArea, null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    sdg_no = models.ForeignKey(Sdg, null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    proj_team = models.ManyToManyField(Researcher, related_name="team", blank=True)
    proj_stakeholder = models.ManyToManyField(Stakeholder, related_name="stakeholder", blank=True)
    impl_agency = models.ForeignKey(CMI, related_name='projects', on_delete=models.CASCADE)
    co_impl_agency = models.ManyToManyField(CMI, related_name='project_co_impl_agency', blank=True)
    coop_agency = models.ManyToManyField(CMI, related_name='coop_agency', blank=True)
    fund_agency = models.ForeignKey(CMI, related_name='+', on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    final_impl_date = models.DateField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    approved_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    approved_date = models.DateField(blank=True, null=True)
    daterequestedext = models.DateField(blank=True, null=True)
    requested_by = models.ForeignKey(Researcher, null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    ext_duration = models.IntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=250, blank=True, null=True)
    proj_file = models.FileField(upload_to='project_files/', blank=True, null=True)
    date_uploaded = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)
    history = HistoricalRecords(excluded_fields=[
        "prog_id",
        "proj_description",
        "status",
        "proj_type",
        "commodity",
        "priority",
        "sdg_no",
        "proj_team",
        "proj_stakeholder",
        "impl_agency",
        "co_impl_agency",
        "coop_agency",
        "fund_agency",
        "start_date",
        "end_date",
        "final_impl_date",
        "duration",
        "approved_budget",
        "approved_date",
        "requested_by",
        "ext_duration",
        "proj_file",
        "date_uploaded",
        "created_at",
        "created_by",
        "modified_at",
        "modified_by",
    ])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "project"


    def snippet(self):
        return self.proj_description[:130] + '...'

auditlog.register(Project, m2m_fields={"commodity", "proj_team", "proj_stakeholder", "co_impl_agency", "coop_agency"})

class ProjectImplementingSite(models.Model):
    projimp = models.AutoField(primary_key=True)
    proj_id = models.ForeignKey(Project, related_name='proj_imp', on_delete=models.CASCADE)
    barangay = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=5, blank=True, null=True)
    geolat = models.FloatField(blank=True, null=True)
    geolong = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)


    class Meta:
        db_table = "proj_imp_site"

auditlog.register(ProjectImplementingSite)


class ProjectOutput(models.Model):
    PUBLICATION = 'Publication'
    PATENT = 'Patent'
    PROPERTY = 'Property'
    PRODUCT = 'Product'
    PEOPLE = 'People'
    PLACE_PARTNERSHIP = 'Place and Partnership'

    OUTPUT_TYPE = (
        (PUBLICATION, 'Publication'),
        (PATENT, 'Patent'),
        (PROPERTY, 'Property'),
        (PRODUCT, 'Product'),
        (PEOPLE, 'People'),
        (PLACE_PARTNERSHIP, 'Place and Partnership'),
    )

    projout_id = models.AutoField(primary_key=True)
    proj_id = models.ForeignKey(Project, related_name='proj_output', on_delete=models.CASCADE)
    proj_output_type = models.CharField(max_length=100, choices=OUTPUT_TYPE, default=PUBLICATION)
    proj_output_desc = models.TextField(blank=True, null=True)
    iec_id = models.ForeignKey(IecMaterial, related_name='+', blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name="+", blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "proj_output"

auditlog.register(ProjectOutput)

