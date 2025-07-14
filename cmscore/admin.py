from django.contrib import admin
from .models import *
# Register your models here.


class SlideAdmin(admin.ModelAdmin):
    list_display = ['name', 'detail', 'image']


admin.site.register(Slide, SlideAdmin)
admin.site.register(Loginbg)
admin.site.register(About)
admin.site.register(Organization)
admin.site.register(Album)
admin.site.register(AlbumPhoto)