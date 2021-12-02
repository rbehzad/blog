from django.urls import path
from .views import *

urlpatterns = [
    path('login/', loginPage, name='login')
]