from django import forms
from consortium.models import CMI
from commodity.models import Commodity
from program.models import Program, Researcher, Stakeholder
from .models import Sdg, Project, PriorityArea, ProjectOutput, ProjectImplementingSite
from commodity.models import IecMaterial


class ProjectForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    prog_id = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    status = forms.ChoiceField(
        choices=Project.CHOICE_STATUS,
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    proj_description = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    proj_type = forms.ChoiceField(
        choices=Project.CHOICE_TYPE,
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    commodity = forms.ModelMultipleChoiceField(
        queryset=Commodity.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    proj_leader = forms.ModelChoiceField(
        queryset=Researcher.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    priority = forms.ModelChoiceField(
        queryset=PriorityArea.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    sdg_no = forms.ModelChoiceField(
        queryset=Sdg.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    proj_team = forms.ModelMultipleChoiceField(
        queryset=Researcher.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    proj_stakeholder = forms.ModelMultipleChoiceField(
        queryset=Stakeholder.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    impl_agency = forms.ModelChoiceField(
        queryset=CMI.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    co_impl_agency = forms.ModelMultipleChoiceField(
        queryset=CMI.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    coop_agency = forms.ModelMultipleChoiceField(
        queryset=CMI.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    fund_agency = forms.ModelChoiceField(
        queryset=CMI.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=False
    )
    final_impl_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=False
    )
    duration = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    approved_budget = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    approved_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=False
    )
    daterequestedext = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=False
    )
    requested_by = forms.ModelChoiceField(
        queryset=Researcher.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    ext_duration = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    proj_file = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    remarks = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
        )

    class Meta:
        model = Project
        fields = [
            'title',
            'prog_id',
            'status',
            'proj_description',
            'proj_type',
            'commodity',
            'proj_leader',
            'priority',
            'sdg_no',
            'proj_team',
            'proj_stakeholder',
            'impl_agency',
            'co_impl_agency',
            'coop_agency',
            'fund_agency',
            'start_date',
            'end_date',
            'final_impl_date',
            'duration',
            'approved_budget',
            'approved_date',
            'daterequestedext',
            'requested_by',
            'ext_duration',
            'proj_file',
            'remarks',
        ]

class SdgForm(forms.ModelForm):
    sdg_title = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    sdg_desc = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control"}
        ),
        required=False
    )

    class Meta:
        model = Sdg
        fields = [
            'sdg_title',
            'sdg_desc',
        ]

class PriorityAreaForm(forms.ModelForm):
    area = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control"}
        ),
        required=False
    )

    class Meta:
        model = PriorityArea
        fields = [
            'area',
            'description',
        ]
class ProjectOutputForm(forms.ModelForm):
    proj_id = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    proj_output_type = forms.ChoiceField(
        choices=ProjectOutput.OUTPUT_TYPE,
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    proj_output_desc = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    iec_id = forms.ModelChoiceField(
        queryset=IecMaterial.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )

    class Meta:
        model = ProjectOutput
        fields = [
            'proj_id',
            'proj_output_type',
            'proj_output_desc',
            'iec_id'
        ]

class ProjectImplementingSiteForm(forms.ModelForm):
    proj_id = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    barangay = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    province = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    zipcode = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    geolat = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    geolong = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )

    class Meta:
        model = ProjectImplementingSite
        fields = [
            'proj_id',
            'barangay',
            'city',
            'province',
            'zipcode',
            'geolat',
            'geolong'
        ]