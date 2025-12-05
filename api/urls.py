from django.urls import path, include
from rest_framework import routers

# Importamos tus nuevas vistas
from .views import (
    health, 
    InfoView, 
    UsuarioViewSet, 
    DepartamentoViewSet, 
    SensorViewSet, 
    EventoViewSet, 
    ComandoRemotoViewSet
)

# Configuración del Router Automático (Crea las rutas GET, POST, PUT, DELETE solas)
router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'sensores', SensorViewSet)
router.register(r'eventos', EventoViewSet)
router.register(r'comandos', ComandoRemotoViewSet)

urlpatterns = [
    # Endpoint simple de salud
    path('health/', health, name='health'),
    
    # Endpoint requerido por el profe (/api/info/)
    # Nota: Como InfoView ahora es una Clase (APIView), usamos .as_view()
    path('info/', InfoView.as_view(), name='info'),
    
    # Incluimos todas las rutas del router
    path('', include(router.urls)),
]