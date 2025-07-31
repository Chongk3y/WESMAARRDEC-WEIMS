import django_filters
from .models import Secretariat

class SecretariatFilter(django_filters.FilterSet):
    position = django_filters.CharFilter(lookup_expr='icontains', label="Position")
    specialization = django_filters.CharFilter(lookup_expr='icontains', label="Specialization")

    class Meta:
        model = Secretariat
        fields = {
                  'consortium_id': ['exact'],
                  'position': ['icontains'],
                  'specialization': ['icontains'],
                }

    def __init__(self, *args, **kwargs):
        super(SecretariatFilter, self).__init__(*args, **kwargs)
        self.filters['consortium_id'].label = 'Consortium'
        self.filters['consortium_id'].extra['empty_label'] = "All"     
        
