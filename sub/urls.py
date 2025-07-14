from django.contrib import admin
from django.urls import path
from sub import views  
 
app_name = 'sub'

urlpatterns = [

    path('',views.home,name='home'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('about_us/',views.about,name='about'),
    path('CMI_summary/',views.summary,name='summary'),
    path('audit_trail/',views.audit_trail,name='audit_trail'),
    path('manage_accounts/',views.manage,name='manage'),

    #-----delete user
    path('delete_account/<username>',views.delete_user,name='delete_user'),
    
    #-----IEC MATERIAL
    path('nav/',views.nav,name='nav'),
    path('IEC_Materials/', views.index_iec, name='iec_material'),  
    path('IEC_Materials/add/',views.add_iecmaterial, name='add_iecmaterial'), 
    path('IEC_Materials/<title>',views.edit_iecmaterial, name='edit_iecmaterial'),
    path('IEC_Materials/view/<title>',views.detail_iecmaterial, name='detail_iecmaterial'),
    path('IEC_Materials/delete/<title>', views.delete_iecmaterial, name='delete_iecmaterial'), 

    #------SDG
    path('SDGs/', views.index_sdg, name='sdg'),  
    path('SDGs/add/',views.add_sdg, name='add_sdg'), 
    path('SDGs/<sdg_title>',views.edit_sdg, name='edit_sdg'),
    path('SDGs/view/<sdg_title>',views.detail_sdg, name='detail_sdg'),
    path('SDGs/delete/<sdg_title>', views.delete_sdg, name='delete_sdg'), 

     #------Researcher
    path('Researchers/', views.index_researcher, name='researcher'),  
    path('Researchers/add/',views.add_researcher, name='add_researcher'), 
    path('Researchers/<researcher_id>',views.edit_researcher, name='edit_researcher'),
    path('Researchers/view/<researcher_id>',views.detail_researcher, name='detail_researcher'),
    path('Researchers/delete/<researcher_id>', views.delete_researcher, name='delete_researcher'),

    #------Stakeholder
    path('Stakeholders/', views.index_stakeholder, name='stakeholder'),  
    path('Stakeholders/add/',views.add_stakeholder, name='add_stakeholder'), 
    path('Stakeholders/<stakeholder_id>',views.edit_stakeholder, name='edit_stakeholder'),
    path('Stakeholders/view/<stakeholder_id>',views.detail_stakeholder, name='detail_stakeholder'),
    path('Stakeholders/delete/<stakeholder_id>', views.delete_stakeholder, name='delete_stakeholder'),

    #------Program Budget
    path('ProgramBudgets/', views.index_progbudg, name='progbudg'),  
    path('ProgramBudgets/add/',views.add_progbudg, name='add_progbudg'), 
    path('ProgramBudgets/<progbdg_id>',views.edit_progbudg, name='edit_progbudg'),
    path('ProgramBudgets/view/<progbdg_id>',views.detail_progbudg, name='detail_progbudg'),
    path('ProgramBudgets/delete/<progbdg_id>', views.delete_progbudg, name='delete_progbudg'),

    #------Priority Area
    path('PriorityAreas/', views.index_prioarea, name='prioarea'),  
    path('PriorityAreas/add/',views.add_prioarea, name='add_prioarea'), 
    path('PriorityAreas/<priority_id>',views.edit_prioarea, name='edit_prioarea'),
    path('PriorityAreas/view/<priority_id>',views.detail_prioarea, name='detail_prioarea'),
    path('PriorityAreas/delete/<priority_id>', views.delete_prioarea, name='delete_prioarea'),

    #------Project Output
    path('ProjectOutputs/', views.index_projout, name='projout'),  
    path('ProjectOutputs/add/',views.add_projout, name='add_projout'), 
    path('ProjectOutputs/<projout_id>',views.edit_projout, name='edit_projout'),
    path('ProjectOutputs/view/<projout_id>',views.detail_projout, name='detail_projout'),
    path('ProjectOutputs/delete/<projout_id>', views.delete_projout, name='delete_projout'),

    #------Project Implementing Site
    path('ProjectImplementingSites/', views.index_projimp, name='projimp'),  
    path('ProjectImplementingSites/add/',views.add_projimp, name='add_projimp'), 
    path('ProjectImplementingSites/<projimp>',views.edit_projimp, name='edit_projimp'),
    path('ProjectImplementingSites/view/<projimp>',views.detail_projimp, name='detail_projimp'),
    path('ProjectImplementingSites/delete/<projimp>', views.delete_projimp, name='delete_projimp'),
]