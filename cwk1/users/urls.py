from django.urls import path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.Login, name='login'),

    path('login', views.main_page, name='main_page'),
    path('register', views.register, name='register'),
    path('rating', views.rating, name='rating'),
    path('average', views.average, name='average'), 
    path('rate', views.rate, name='rate'), 
    path('mod_list', views.list, name='list'), 
    path('view',views.view,name='view'),
]