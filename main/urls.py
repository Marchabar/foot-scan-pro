from django.contrib import admin
from django.urls import path, include
from main import views
from main import populate


urlpatterns = [
    path('', views.index),
    path('cargar-db/', populate.cargar, name='cargar-db'),
    path('listado-equipos/', views.listado_equipos, name='listado-equipos'),
    
]