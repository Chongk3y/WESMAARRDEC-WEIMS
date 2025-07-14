from django.urls import path
from . import views
from cmsblg.views import *

urlpatterns = [
    path('search/', views.search, name='search'),
    path('facts/', views.facts, name='facts'),
    path('categorycreateview/', CategoryCreateView.as_view(), name='categorycreateview'),
    path('<slug:slug>/', views.category, name='category_detail'),
    path('posts/<slug:cat>/', views.event, name='posts'), #this is the posts/categories detailed should change it's name but I am time restriced I am very sorry
    path('my_posts/', views.MyPosts, name='myposts'),
    path('all_posts/', views.Posts, name='allposts'),
    path('Details/<slug:category_slug>/<slug:slug>/', detail, name='detail'),
    path('<slug:slug>/', views.category, name='category_detail'),
    path('New_Posts/', views.create_post, name ='newposts'),
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),
    path('View_posts/', view_posts, name= 'view_posts'),
    path('Add_Post/', add_post, name='add_post'),
    path('Edit_Post/<int:pk>', edit_post, name='edit_post'),
    path('Delete_Post/<int:pk>', delete_post, name='delete_post'),
    path('Add_Fact/', add_fact, name='add_fact'),
    path('Edit_Fact/<int:fact_id>', edit_fact, name='edit_fact'),
    path('Delete_Fact/<int:fact_id>', delete_fact, name='delete_fact'),
    path('Add_Category/', add_category, name='add_category'),
    path('Edit_Category/<int:category_id>', edit_category, name='edit_category'),
    path('Delete_Category/<int:category_id>', delete_category, name='delete_category'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment')
    
]