from django.urls import path

from .views import *

urlpatterns = [
    path('home/', HomeListView.as_view(), name='home'),
    path('post-detail/<slug:slug_text>', post_detail),
    path('category/<slug:slug_text>', class_category, name='category_reverse'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerUser, name='register'),
    path('add-post/', addPost, name='add_post'),
    path('add-category/', addCategory, name='add_category'),
    path('add-tag/', addTag, name='add_tag'),
    
    path('delete-category/', deleteCategory, name='delete_category'),
    path('delete-tag/', deleteTag, name='delete_tag'),
]
