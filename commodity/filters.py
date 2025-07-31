import django_filters
from .models import Commodity

class CommodityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name' )

    class Meta:
        model = Commodity
        fields = {'cmi_name': ['exact'],
                  'name': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super(CommodityFilter, self).__init__(*args, **kwargs)
        self.filters['cmi_name'].label = 'CMI'
        self.filters['cmi_name'].extra['empty_label'] = "All"     
        

class CommodityFilterDB(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name' )

    class Meta:
        model = Commodity
        fields = {'cmi_name': ['exact'],
                  'name': ['icontains'],
        }


    def __init__(self, *args, **kwargs):
        super(CommodityFilterDB, self).__init__(*args, **kwargs)
        self.filters['cmi_name'].label = 'CMI'
        self.filters['cmi_name'].extra['empty_label'] = "All"     