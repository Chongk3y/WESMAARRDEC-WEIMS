import django_filters
from .models import Project


class ProjectFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label="Title")

    class Meta:
        model = Project
        fields = {'proj_type': ['exact'],
                  'status': ['exact'],
                  'impl_agency': ['exact'],
                'title': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super(ProjectFilter, self).__init__(*args, **kwargs)
        self.filters['proj_type'].label = 'Types'
        self.filters['proj_type'].extra['empty_label'] = "All"
        self.filters['status'].label = 'Status'
        self.filters['status'].extra['empty_label'] = "All"
        self.filters['impl_agency'].label = 'Implementing Agency'
        self.filters['impl_agency'].extra['empty_label'] = "All"
        

class ProjectFilterDB(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label="Title")

    class Meta:
        model = Project
        fields = {'proj_type': ['exact'],
                  'proj_leader': ['exact'],
                  'status': ['exact'],
                  'impl_agency': ['exact'],
                  'title': ['icontains'],
        }



    def __init__(self, *args, **kwargs):
        super(ProjectFilterDB, self).__init__(*args, **kwargs)
        self.filters['proj_type'].label = 'Types'
        self.filters['proj_type'].extra['empty_label'] = "All"
        self.filters['proj_leader'].label = 'Project Leader'
        self.filters['proj_leader'].extra['empty_label'] = "All"
        self.filters['status'].label = 'Status'
        self.filters['status'].extra['empty_label'] = "All"
        self.filters['impl_agency'].label = 'Implementing Agency'
        self.filters['impl_agency'].extra['empty_label'] = "All"