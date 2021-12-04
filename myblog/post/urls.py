from django.urls import path
from .views import *


urlpatterns = [
    path('home/', HomeListView.as_view()),
    path('post-detail/<slug:slug_text>', post_detail),
    path('category/<slug:slug_text>', class_category, name='category_reverse'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
]
