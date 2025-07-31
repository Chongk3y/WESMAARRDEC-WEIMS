from django.contrib import admin
from django.urls import path
from project import views
 
 
app_name = 'project'

urlpatterns = [
     path('projects/', project, name="project"),
     path('On-GoingProjects/', onproject, name="onproject"),
     path('CompletedProjects/', finproject, name="finproject"),
     path('project/<int:proj_id>/', project_detail, name='project_detail'),
     path('View_projects/', project_view, name = 'project_view'),
     path('Add_projects/', add_project, name = 'add_project'),
     path('Edit_projects/<int:proj_id>', edit_project, name = 'edit_project'),
     path('Delete_projects/<int:proj_id>', delete_project, name = 'delete_project'),
     path('View_sdg/', view_sdg, name='view_sdg'),
     path('Add_sdg/', add_sdg, name='add_sdg'),
     path('Edit_sdg/<int:sdg_no>', edit_sdg, name='edit_sdg'),
     path('Delete_sdg/<int:sdg_no>', delete_sdg, name='delete_sdg'),
     path('priority_areas/', priority_area_view, name='view_priority_areas'),
     path('priority_areas/create/', add_priority_area, name='add_priority_area'),
     path('priority_areas/<int:priority_area_id>/edit/', edit_priority_area, name='edit_priority_area'),
     path('priority_areas/<int:priority_area_id>/delete/', delete_priority_area, name='delete_priority_area'),
     path('project_outputs/', view_project_outputs, name='view_project_outputs'),
     path('project_outputs/add/', add_project_output, name='add_project_output'),
     path('project_outputs/<int:projout_id>/edit/', edit_project_output, name='edit_project_output'),
     path('project_outputs/<int:projout_id>/delete/', delete_project_output, name='delete_project_output'),
     path('project_implementing_sites/', view_project_implementing_sites, name='view_project_implementing_sites'),
     path('project_implementing_sites/add/', add_project_implementing_site, name='add_project_implementing_site'),
     path('project_implementing_sites/<int:site_id>/edit/', edit_project_implementing_site, name='edit_project_implementing_site'),
     path('project_implementing_sites/<int:site_id>/delete/', delete_project_implementing_site, name='delete_project_implementing_site'),
     path('report/project/<int:proj_id>/', generate_project_report, name='generate_project_report'),
]