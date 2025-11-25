from django.contrib import admin
from django.urls import path, include
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
    path('stock-ingredientes/', views.stock_ingredientes, name='stock_ingredientes'),
    path('ingredientes/crear/', views.crear_ingrediente, name='crear_ingrediente'),
    path('plato/<int:plato_id>/deshabilitar/', views.deshabilitar_plato, name='deshabilitar_plato'),
    path('plato/<int:plato_id>/habilitar/', views.habilitar_plato, name='habilitar_plato'),
    path('', include('mainApp.api_urls')),  # Incluye las rutas de la API
    path('api/', include('mainApp.api_urls')),  # Para login/logout en la API

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
