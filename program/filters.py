import django_filters
from .models import Program


class ProgramFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label="Title")

    class Meta:
        model = Program
        fields = {'status': ['exact'],
                'program_leader': ['exact'],
                'impl_agency': ['exact'],
                'title': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super(ProgramFilter, self).__init__(*args, **kwargs)
        self.filters['status'].label = 'Status'
        self.filters['status'].extra['empty_label'] = "All Status"
        self.filters['impl_agency'].label = 'Implementing Agency'
        self.filters['impl_agency'].extra['empty_label'] = "All Agencies"
        self.filters['program_leader'].label = 'Leader'
        self.filters['program_leader'].extra['empty_label'] = "All"
        

class ProgramFilterDB(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label="Title")

    class Meta:
        model = Program
        fields = { 'impl_agency': ['exact'],
                   'status': ['exact'],
                   'program_leader': ['exact'],
                   'funding_agency': ['exact'],
                   'title': ['icontains'],
        }

        
    def __init__(self, *args, **kwargs):
        super(ProgramFilterDB, self).__init__(*args, **kwargs)
        self.filters['impl_agency'].label = 'Implementing Agency'
        self.filters['impl_agency'].extra['empty_label'] = "All"
        self.filters['status'].label = 'Status'
        self.filters['status'].extra['empty_label'] = "All"
        self.filters['program_leader'].label = 'Leader'
        self.filters['program_leader'].extra['empty_label'] = "All"
        self.filters['funding_agency'].label = 'Funding Agency'
        self.filters['funding_agency'].extra['empty_label'] = "All"