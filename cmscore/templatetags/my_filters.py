# in your app's `templatetags` directory, create a new file called `my_filters.py`
from django import template

register = template.Library()

@register.filter
def filter_deleted_images(images):
    return images.exclude(is_deleted=True)
