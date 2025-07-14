from django.urls import path
from .views import register

 
app_name = 'team'

urlpatterns = [
    path('Cluster/',views.view_team,name='view_team'),
    path('Add_member/',views.add_team,name='add_team'),
    path('Edit_member/<int:member_id>/',views.edit_team, name='edit_team'),
    path('Delete_member/<int:member_id>/', delete_team, name='delete_team'),
]