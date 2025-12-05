from django.urls import path, include
from rest_framework import routers

# Importamos las vistas para el Login (JWT)
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
    ComandoRemotoViewSet
)

# Configuración del Router Automático
router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'sensores', SensorViewSet)
router.register(r'eventos', EventoViewSet)
router.register(r'comandos', ComandoRemotoViewSet)

urlpatterns = [
    # --- RUTAS DE AUTENTICACIÓN (LOGIN) ---
    # POST /api/token/         -> Envías usuario/pass y te devuelve el Token (Login)
    # POST /api/token/refresh/ -> Envías el refresh token y te da uno nuevo
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # --- TUS ENDPOINTS ---
    path('health/', health, name='health'),
    path('info/', InfoView.as_view(), name='info'), # Requerimiento /api/info/
    
    # Incluimos el resto (CRUDs)
    path('', include(router.urls)),
]