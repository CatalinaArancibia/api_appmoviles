from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Importamos tus vistas
from .views import (
    health, 
    InfoView, 
    UsuarioViewSet, 
    DepartamentoViewSet, 
    SensorViewSet, 
    EventoViewSet, 
    ComandoRemotoViewSet,
    simular_acceso  
)

# Configuración del Router
router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'sensores', SensorViewSet)
router.register(r'eventos', EventoViewSet)
router.register(r'comandos', ComandoRemotoViewSet)

urlpatterns = [
    # 1. Rutas para el Login (JWT)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 2. Rutas manuales
    path('health/', health, name='health'),
    path('info/', InfoView.as_view(), name='info'),
    
    # 3. Ruta para la simulación de acceso (El Cerebro)
    path('simular-acceso/', simular_acceso, name='simular_acceso'),
    
    # 4. Rutas automáticas del router (CRUDs)
    path('', include(router.urls)),
]