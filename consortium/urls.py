from django.contrib import admin
from django.urls import path
from consortium import views

app_name = 'consortium'

urlpatterns = [
   path('CMI_view/', CMI_View, name='CMI_View'),
   path('edit_consortium/<int:consortium_id>', edit_Consortium, name='edit_Consortium'),
   path('add_CMI/', add_CMI, name='add_CMI'),
   path('edit_CMI/<int:agency_id>/', edit_CMI, name='edit_CMI'),
   path('delete_CMI/<int:agency_id>/', delete_CMI, name='delete_CMI'),
   path('report/cmi/<int:agency_id>/', generate_cmi_report, name='cmi_report')
]