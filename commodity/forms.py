from django import forms  
from django.forms import ModelForm
from commodity.models import Commodity, IecMaterial
from consortium.models import CMI

class CommodityForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    cmi_name = forms.ModelChoiceField(
        queryset=CMI.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    detail = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    img = forms.ImageField(
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    produced_by = forms.CharField(
        widget=forms.Textarea(
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
        model = Commodity
        fields = [
            'name', 
            'cmi_name', 
            'detail', 
            'img', 
            'produced_by', 
            'geolat', 
            'geolong',
        ]

class IecMaterialForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    iec_type = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    commodity = forms.ModelChoiceField(
        queryset=Commodity.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    target_audience = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    designed_by = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    content_by = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    date_published = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=False
    )
    ip = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    iec_file = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        ),
        required=False
    )

    class Meta:
        model = IecMaterial
        fields = [
            'title', 
            'iec_type', 
            'commodity', 
            'target_audience', 
            'designed_by', 
            'content_by', 
            'date_published', 
            'ip', 
            'iec_file',
        ]