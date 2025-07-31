import django_filters
from .models import CMI


class CMIFilter(django_filters.FilterSet):
    agency_code = django_filters.CharFilter(lookup_expr='icontains', label='Code' )
    address = django_filters.CharFilter(lookup_expr='icontains', label='Address')
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')


    class Meta:
        model = CMI
        fields = {
                'consortium_id': ['exact'],
                'name': ['icontains'],
                'agency_code': ['icontains'],
                'address': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super(CMIFilter, self).__init__(*args, **kwargs)
        self.filters['consortium_id'].label = 'Consortium'
        self.filters['consortium_id'].extra['empty_label'] = "All"   
