from django.contrib import admin
from django.urls import path
from program import views  
 
app_name = 'program'

urlpatterns = [
    path('Programs/', views.program, name='program'),  
    path('programs/<prog_id>/',views.program_detail, name='program_details'), 
    path('View_Programs/', views.program_View, name='program_View'), 
    path('Add_program/', views.add_view, name ='add_program'),
    path('Edit_program/<int:prog_id>', views.edit_program, name ='edit_program'),
    path('Delete_program/<int:prog_id>', views.delete_program, name ='delete_program'),
    path('View_researcher/', View_researcher, name= 'View_researcher'),
    path('Add_researcher/', add_researcher, name='add_researcher'),
    path('Edit_researcher/<int:researcher_id>', edit_researcher, name='edit_researcher'),
    path('Delete_researcher/<int:researcher_id>', delete_researcher, name='delete_researcher'),
    path('View_stakeholders/', View_stakeholders, name= 'View_stakeholders'),
    path('Add_stakeholders/', add_stakeholders, name='add_stakeholders'),
    path('Edit_stakeholders/<int:stakeholder_id>', edit_stakeholders, name='edit_stakeholders'),
    path('Delete_stakeholders/<int:stakeholder_id>', delete_stakeholders, name='delete_stakeholders'),
    path('View_Program_Budget/', view_program_budget, name= 'view_program_budget'),
    path('Add_Program_Budget/', add_program_budget, name='add_program_budget'),
    path('Edit_Program_Budget/<int:progbdg_id>', edit_program_budget, name='edit_program_budget'),
    path('Delete_Program_Budget/<int:progbdg_id>', delete_program_budget, name='delete_program_budget')
]