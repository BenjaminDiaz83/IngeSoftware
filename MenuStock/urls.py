from django.contrib import admin
from django.urls import path
from mainApp import views
from django.conf import settings
from django.conf.urls.static import settings, static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('administrador', views.listar_platos, name='lista_platos'),
    path('crear/', views.crear_plato, name='crear_plato'), 
    path('editar/<int:pk>/', views.editar_plato, name='editar_plato'), 
    path('eliminar/<int:pk>/', views.eliminar_plato, name='eliminar_plato'),
    path('', views.administrador, name='administrador'), 
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
