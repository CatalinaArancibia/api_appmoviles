from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Importamos los Modelos Nuevos
from .models import Usuario, Departamento, Sensor, Evento, ComandoRemoto
# Importamos los Serializadores (que crearemos/actualizaremos en el siguiente paso)
from .serializers import (
    UsuarioSerializer, 
    DepartamentoSerializer, 
    SensorSerializer, 
    EventoSerializer, 
    ComandoRemotoSerializer
)

# ==============================================================================
# 1. PERMISOS PERSONALIZADOS (Requerimiento 7)
# ==============================================================================
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado:
    - Admin: Tiene acceso total (GET, POST, PUT, DELETE).
    - Operador/Usuario: Solo puede ver (GET).
    """
    def has_permission(self, request, view):
        # Si es una petición segura (GET, HEAD, OPTIONS), dejar pasar a cualquiera autenticado
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Para escribir (POST, PUT, DELETE), el usuario debe ser Admin
        return request.user and request.user.is_authenticated and request.user.rol == 'admin'


# ==============================================================================
# 2. ENDPOINTS BÁSICOS (Info y Health)
# ==============================================================================
def health(request):
    """Endpoint simple para verificar que el servidor vive"""
    return JsonResponse({"status": "ok", "server": "django-iot"})

class InfoView(APIView):
    """
    Endpoint público requerido (/api/info/)
    Devuelve JSON con datos del proyecto.
    """
    permission_classes = [] # Público, no requiere Token

    def get(self, request):
        data = {
            "autor": ["Catalina Arancibia"],
            "asignatura": "Programación Back End",
            "proyecto": "Smart Barrier IoT",
            "descripcion": "Sistema de control de acceso vehicular con RFID y App Móvil",
            "version": "1.0"
        }
        return Response(data, status=status.HTTP_200_OK)


# ==============================================================================
# 3. VIEWSETS (CRUDs COMPLETOS)
# ==============================================================================

# CRUD DEPARTAMENTOS
class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    # Solo el admin puede crear deptos, el operador solo verlos
    permission_classes = [IsAdminOrReadOnly]

# CRUD USUARIOS
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdminOrReadOnly]

# CRUD SENSORES (RFID)
class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAdminOrReadOnly]

# CRUD EVENTOS (Historial)
class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    # Aquí cambiamos la lógica un poco:
    # Quizás quieres que todos puedan ver el historial, pero NADIE pueda borrarlo por seguridad.
    # Por ahora usamos el permiso estándar definido arriba.
    permission_classes = [permissions.IsAuthenticated] 

# CRUD COMANDOS REMOTOS
class ComandoRemotoViewSet(viewsets.ModelViewSet):
    queryset = ComandoRemoto.objects.all()
    serializer_class = ComandoRemotoSerializer
    permission_classes = [permissions.IsAuthenticated]