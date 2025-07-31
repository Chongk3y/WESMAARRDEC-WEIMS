from django.contrib import admin
from django.urls import path
from commodity import views  
 
app_name = 'commodity'

urlpatterns = [
    path('commodities/add_Commodity/',views.add_commodity, name='add_commodity'),  
    path('commodities/<int:com_id>/', commodity_detail, name='commodetail'),
    path('View_Commodity/', view_commodity, name = "view_commodity"),
    path('Add_Commodity/', add_commodity, name = "add_commodity"),
    path('Edit_Commodity/<int:com_id>', edit_commodity, name = "edit_commodity"),
    path('Delete_Commodity/<int:com_id>', delete_commodity, name = "delete_commodity"),
    path('View_IEC/', view_IEC, name = 'view_IEC'),
    path('Add_IEC/', add_IEC, name = 'add_IEC'),
    path('Edit_IEC/<int:iec_id>', edit_IEC, name='edit_IEC'),
    path('Delete_IEC/<int:iec_id>', delete_IEC, name='delete_IEC'),
]