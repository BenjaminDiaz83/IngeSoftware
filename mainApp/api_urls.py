# mainApp/api_urls.py

from rest_framework.routers import DefaultRouter
from mainApp import views 

router = DefaultRouter()

# Genera los endpoints: /platos/ y /platos/{pk}/
router.register(r'platos', views.PlatoViewSet)

# Genera los endpoints: /ingredientes/ y /ingredientes/{pk}/
router.register(r'ingredientes', views.IngredienteViewSet)

urlpatterns = router.urls