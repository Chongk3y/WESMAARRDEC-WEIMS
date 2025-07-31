from django import forms  
from .models import Secretariat 
from consortium.models import Consortium
from django import forms
from .models import Secretariat


class SecretariatForm(forms.ModelForm):
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
        required=False, 
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    position = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    manager = forms.ModelChoiceField(
        queryset=Secretariat.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    consortium_id = forms.ModelChoiceField(
        queryset=Consortium.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    email_add = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    contact_no = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    date_appointed = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=True
    )
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=True
    )
    organization = forms.ChoiceField(
          choices=[
                ('DOST-PCAARD', 'DOST-PCAARD'),
                ('Consortium', 'Consortium'),
            ],
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    sex = forms.ChoiceField(
          choices=[
                ('Male', 'Male'),
                ('Female', 'Female'),
            ],
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    bach_deg = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    bdyearcompleted = forms.IntegerField(
        required=False, 
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        )
    )
    mas_deg = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    mdyearcompleted = forms.IntegerField(
        required=False, 
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        )
    )
    doc_deg = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    ddyearcompleted = forms.IntegerField(
        required=False, 
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        )
    )
    specialization = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    photo = forms.ImageField(
       required=False, 
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control'}
        )
    )
    pds_file = forms.FileField(
        required=False, 
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        )
    )

    class Meta:
        model = Secretariat
        fields = [
            'fname', 
            'lname', 
            'mname', 
            'position', 
            'manager', 
            'consortium_id', 
            'email_add', 
            'contact_no', 
            'date_appointed', 
            'dob', 
            'sex', 
            'bach_deg', 
            'bdyearcompleted', 
            'mas_deg', 
            'mdyearcompleted', 
            'doc_deg', 
            'ddyearcompleted', 
           'organization',
            'specialization', 
            'photo', 
            'pds_file'
        ]
        widgets = {
            'date_appointed': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }


class SecretariatEditForm(forms.ModelForm):
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
        required=False, 
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    position = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    manager = forms.ModelChoiceField(
        queryset=Secretariat.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=False
    )
    consortium_id = forms.ModelChoiceField(
        queryset=Consortium.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    email_add = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    contact_no = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    date_appointed = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=True
    )
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=True
    )
    organization = forms.ChoiceField(
          choices=[
                ('DOST-PCAARD', 'DOST-PCAARD'),
                ('Consortium', 'Consortium'),
            ],
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    sex = forms.ChoiceField(
          choices=[
                ('Male', 'Male'),
                ('Female', 'Female'),
            ],
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        required=True
    )
    bach_deg = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    bdyearcompleted = forms.IntegerField(
        required=False, 
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        )
    )
    mas_deg = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    mdyearcompleted = forms.IntegerField(
        required=False, 
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        )
    )
    doc_deg = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    ddyearcompleted = forms.IntegerField(
        required=False, 
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        )
    )
    specialization = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )
    photo = forms.ImageField(
       required=False, 
        widget=forms.ClearableFileInput(
            attrs={'class': 'form-control'}
        )
    )
    pds_file = forms.FileField(
        required=False, 
        widget=forms.FileInput(
            attrs={"class": "form-control"}
        )
    )

    class Meta:
        model = Secretariat
        fields = [
            'fname', 
            'lname', 
            'mname', 
            'position', 
            'manager', 
            'consortium_id', 
            'email_add', 
            'contact_no', 
            'date_appointed', 
            'dob', 
            'sex', 
            'organization',
            'bach_deg', 
            'bdyearcompleted', 
            'mas_deg', 
            'mdyearcompleted', 
            'doc_deg', 
            'ddyearcompleted', 
            'specialization', 
            'photo', 
            'pds_file'
        ]
        widgets = {
            'date_appointed': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }