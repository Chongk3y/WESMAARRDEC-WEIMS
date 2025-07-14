from django import forms  
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Team  
from consortium.models import CMI


class TeamForm(forms.ModelForm):
    fname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    lname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    mname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}), 
        required=False)

    position = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    cmi = forms.ModelChoiceField(
        queryset=CMI.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control"}))

    teams = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    email_add = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control"}))

    contact_no = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    date_appointed = forms.DateField(
         widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}), 
        required=False)

    sex = forms.ChoiceField(
        choices=Team.CHOICE_SEX,
        widget=forms.Select(
            attrs={
                "class": "form-control"}))

    specialization = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}), 
        required=False)

    photo = forms.ImageField(
        required=False, 
        widget=forms.ClearableFileInput
            (attrs={
                "class": "form-control"}))

    pds_file = forms.FileField(
        required=False, 
        widget=forms.ClearableFileInput
            (attrs={
                "class": "form-control"}))

    class Meta:
        model = Team
        fields = ('fname', 'lname', 'mname', 'position', 'cmi', 'teams', 
                  'email_add', 'contact_no', 'date_appointed', 'sex', 
                  'specialization', 'photo', 'pds_file')

class TeamMemberFilterForm(forms.Form):
    q_name = forms.CharField(required=False)
    q_team = forms.CharField(required=False)
    cmis = forms.ModelChoiceField(queryset=CMI.objects.all(), required=False)
