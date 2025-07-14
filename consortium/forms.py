from django import forms
from consortium.models import CMI, Consortium


class CMIForm(forms.ModelForm):
    agency_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    is_cmi = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input"}),
        required=False)

    consortium_id = forms.ModelChoiceField(
        queryset=Consortium.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control"}))

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    geolat = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"}),
        required=False)

    geolong = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"}),
        required=False)

    logo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput
            (attrs=
                {'class': 'form-control'}))

    detail = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control"}),
        required=False)

    contact_no = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}),
        required=False)

    telno = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}),
        required=False)

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control"}),
        required=False)

    url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                "class": "form-control"}),
        required=False)

    status = forms.ChoiceField(
        choices=CMI.CHOICE_STATUS,
        widget=forms.Select(
            attrs={
                "class": "form-control"}))

    remarks = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control"}),
        required=False)

    class Meta:
        model = CMI
        fields = ('agency_code', 'name', 'is_cmi', 'consortium_id', 'address',
                  'geolat', 'geolong', 'logo', 'detail', 'contact_no', 'telno',
                  'email', 'url', 'status', 'remarks')
        labels={
            'pds_file': 'Personal Data Sheet (PDS)',
            'geolat' : 'Latitude',
            'geolong' : 'Longitude'}


class ConsortiumForm(forms.ModelForm):
    consortium_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    consortium_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    consortium_address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    geolat = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"}),
        required=False)

    geolong = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"}),
        required=False)

    consortium_logo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput
            (attrs=
                {'class': 'form-control'}))

    mission = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control"}),
        required=False)

    vision = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control"}),
        required=False)

    consortium_desc = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control"}),
        required=False)

    consortium_objectives = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control"}),
        required=False)

    url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                "class": "form-control"}),
        required=False)

    fb_url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                "class": "form-control"}),
        required=False)

    yt_url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                "class": "form-control"}),
        required=False)

    telno = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}),
        required=False)

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control"}),
        required=False)

    class Meta:
        model = Consortium
        fields = ('consortium_code', 'consortium_name', 'consortium_address',
                  'geolat', 'geolong', 'consortium_logo', 'mission', 'vision',
                  'consortium_desc', 'consortium_objectives', 'url', 'fb_url',
                  'yt_url', 'telno', 'email')
        labels={
            'geolat' : 'Latitude',
            'geolong' : 'Longitude'}
