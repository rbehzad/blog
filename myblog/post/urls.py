from django.urls import path
from .views import HomeListView, post_detail, class_category
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('home/', HomeListView.as_view()),
    path('post-detail/<slug:slug_text>', post_detail),
    path('category/<slug:slug_text>', class_category, name='category_reverse'),  
]

urlpatterns += staticfiles_urlpatterns()