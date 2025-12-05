from django.urls import path, include
from .views import health, info
from rest_framework import routers
from .views import CategoriaViewSet, ProductoViewSet

router = routers.DefaultRouter()
router.register('categorias', CategoriaViewSet)
router.register('productos', ProductoViewSet)

urlpatterns = [
    path('health/', health),
    path('info/', info),
    path('', include(router.urls)),
]
