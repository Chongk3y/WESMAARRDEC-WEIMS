from django.contrib import admin
from django.urls import path
from .views import *
 
app_name = 'secretariat'

urlpatterns = [
    path('secretariat/', secretariatview, name= 'secretariatview'),
    path('add_secretariat/', add_secretariat, name='add_secretariat'),
    path('delete_secretariat/<int:secretariat_id>/', delete_secretariat, name='delete_secretariat'),
    path('edit_secretariat/<int:secretariat_id>/', edit_secretariat, name='edit_secretariat'),
    path('secretariat_hierarchy/', secretariat_hierarchy, name='secretariat_hierarchy'),
]