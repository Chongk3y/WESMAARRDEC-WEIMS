from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"}))

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"}))

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    profile_picture = forms.ImageField(
        required=False, 
        widget=forms.ClearableFileInput
            (attrs=
                {'class': 'form-control'}))

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"}))

    error_messages = {
        'password_too_short': "Your password must contain at least %(min_length)d characters.",
        'password_too_common': "Your password is too common.",
        'password_entirely_numeric': "Your password can't be entirely numeric.",
        'password_similar_to_username': "Your password can't be too similar to your other personal information.",
        'password_mismatch': "The two password fields didn't match.",
    }

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                password_validation.validate_password(password1, self.instance)
            except forms.ValidationError as error:
                self.add_error('password1', error)
        return password1

    class Meta:
        model = User
        fields = ('username', 'email','profile_picture', 'password1', 'password2', 'researcher', 'secretariat', 'stakeholder', 'is_superuser', 'first_name', 'last_name')

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", "placeholder":"Username"}))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control", "placeholder":"Password"}))

class EditUserForm(forms.ModelForm):

    profile_picture = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    researcher = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    secretariat = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    stakeholder = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active','profile_picture', 'researcher', 'secretariat', 'stakeholder']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
        }
