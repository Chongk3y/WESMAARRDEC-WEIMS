from django import template
from consortium.models import CMI

register = template.Library()

@register.inclusion_tag('cmi_list.html')
def get_cmi_list():
    cmi_list = CMI.objects.filter(status='Active')
    return {'cmi_list': cmi_list}