from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Program, Researcher, Stakeholder, ProgramBudget

# Register your models here.
admin.site.register(Program, SimpleHistoryAdmin)
admin.site.register(Researcher)
admin.site.register(Stakeholder)
admin.site.register(ProgramBudget)