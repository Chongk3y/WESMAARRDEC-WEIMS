from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = "auth_user"

urlpatterns = [
path('registration/',views.nav,name='registration'),
path('login/', login, name='login'),
path('logout/', logout_view, name='logout'),
path('accounts/', accountman, name='accountman'),
path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
path('change_password/', change_password, name='change_password'),
path('reset_password/<int:user_id>/', reset_password, name='reset_password')
]