from django import forms  
from .models import Program, Researcher, Stakeholder, ProgramBudget
from consortium.models import CMI, Consortium
from commodity.models import Commodity  
from django.forms.widgets import Widget, CheckboxInput
from django import forms

class ProgramForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    status = forms.ChoiceField(
        choices=Program.CHOICE_STATUS,
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    prog_description = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    program_leader = forms.ModelChoiceField(
        queryset=Researcher.objects.all(),
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
    impl_agency = forms.ModelChoiceField(
        queryset=CMI.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    co_impl_agency = forms.ModelMultipleChoiceField(
        queryset=CMI.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    funding_agency = forms.ModelChoiceField(
        queryset=CMI.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=False
    )
    duration = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    final_impl_date = forms.DateField(
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
    prog_file = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )

    class Meta:
        model = Program
        fields = [
            'title', 
            'status', 
            'prog_description', 
            'program_leader', 
            'commodity', 
            'impl_agency', 
            'co_impl_agency', 
            'funding_agency', 
            'start_date', 
            'duration', 
            'final_impl_date', 
            'daterequestedext', 
            'requested_by', 
            'ext_duration', 
            'prog_file'
        ]



class ResearcherForm(forms.ModelForm):
    fname = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    lname = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    mname = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    cmi = forms.ModelChoiceField(
        queryset=CMI.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    contact_no = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=False
    )
    sex = forms.ChoiceField(
        choices=Researcher.CHOICE_SEX,
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    specialization = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    photo = forms.ImageField(
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    pds_file = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )

    class Meta:
        model = Researcher
        fields = [
            'fname', 
            'lname', 
            'mname', 
            'cmi', 
            'address', 
            'email', 
            'contact_no', 
            'dob', 
            'sex', 
            'specialization', 
            'photo', 
            'pds_file'
        ]

class StakeholderForm(forms.ModelForm):
    fname = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    lname = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    mname = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    consortium_id = forms.ModelChoiceField(
        queryset=Consortium.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    commodity = forms.ModelMultipleChoiceField(
        queryset=Commodity.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    sex = forms.CharField(
        widget=forms.Select(
            attrs={"class": "form-control"},
            choices=Stakeholder.CHOICE_SEX 
        ),
        required=False
    )
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=False
    )
    barangay = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
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
    email_add = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    contact_no = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    photo = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )

    class Meta:
        model = Stakeholder
        fields = [
            'fname', 
            'lname', 
            'mname', 
            'consortium_id', 
            'commodity', 
            'sex', 
            'dob', 
            'barangay', 
            'city', 
            'province', 
            'zipcode', 
            'email_add', 
            'contact_no', 
            'photo'
        ]

class ProgramBudgetForm(forms.ModelForm):
    prog_id = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    yr = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    fund_source = forms.ModelChoiceField(
        queryset=CMI.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    ps = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    mooe = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    eo = forms.FloatField(
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )

    class Meta:
        model = ProgramBudget
        fields = [
            'prog_id', 
            'yr', 
            'fund_source', 
            'ps', 
            'mooe', 
            'eo'
        ]