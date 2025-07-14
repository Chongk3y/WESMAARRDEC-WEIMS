from django.contrib import admin
from .models import Commodity, IecMaterial

# Register your models here.
admin.site.register(Commodity)
admin.site.register(IecMaterial)