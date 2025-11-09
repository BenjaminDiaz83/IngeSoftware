from django.contrib import admin
from django.urls import path
from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('administrador', views.listar_platos, name='lista_platos'),
    path('crear/', views.crear_plato, name='crear_plato'), 
    path('editar/<int:pk>/', views.editar_plato, name='editar_plato'), 
    path('eliminar/<int:pk>/', views.eliminar_plato, name='eliminar_plato'),
    path('', views.administrador, name='administrador'), 
]
