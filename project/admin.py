from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Sdg)
admin.site.register(Project)
admin.site.register(PriorityArea)
admin.site.register(ProjectImplementingSite)
admin.site.register(ProjectOutput)

