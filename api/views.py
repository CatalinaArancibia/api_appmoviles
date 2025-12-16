from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Importamos los Modelos
from .models import Usuario, Departamento, Sensor, Evento, ComandoRemoto

# Importamos los Serializadores
from .serializers import (
    UsuarioSerializer, 
    DepartamentoSerializer, 
    SensorSerializer, 
    EventoSerializer, 
    ComandoRemotoSerializer
)

# ==============================================================================
# 1. PERMISOS PERSONALIZADOS (ADMIN vs OPERADOR) - VERSIÓN ESTRICTA
# ==============================================================================
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso estricto:
    - Admin: Puede hacer TODO (Crear, Leer, Actualizar, Borrar).
    - Operador/Usuario: Solo puede LEER (GET).
    """
    def has_permission(self, request, view):
        # 1. Si el usuario no está autenticado, denegar siempre
        if not request.user or not request.user.is_authenticated:
            print(f"DEBUG: Usuario no autenticado")
            return False

        # 2. Si es una petición segura (GET, HEAD, OPTIONS), permitir a cualquiera autenticado
        if request.method in permissions.SAFE_METHODS:
            return True

        # 3. DEBUG: Imprimimos en la consola de AWS quién está intentando escribir
        user_rol = getattr(request.user, 'rol', 'SIN_ROL')
        print(f"DEBUG: Intento de escritura por Usuario: {request.user.username}, Rol: {user_rol}, Superuser: {request.user.is_superuser}")

        # 4. Para escribir (POST, PUT, DELETE), validamos ESTRICTAMENTE
        if request.user.is_superuser:
            return True
            
        if str(user_rol) == 'admin':
            return True
            
        # Si llega aquí, es operador intentando escribir -> DENEGAR
        return False


# ==============================================================================
# 2. MANEJADORES DE ERROR GLOBALES
# ==============================================================================
def error_404_handler(request, exception=None):
    return JsonResponse({
        "error": "Ruta no encontrada",
        "codigo": 404,
        "mensaje": "El endpoint solicitado no existe. Verifica la URL."
    }, status=404)

def error_500_handler(request):
    return JsonResponse({
        "error": "Error Interno del Servidor",
        "codigo": 500,
        "mensaje": "Ocurrió un problema inesperado. Intenta más tarde."
    }, status=500)


# ==============================================================================
# 3. ENDPOINTS BÁSICOS
# ==============================================================================
@api_view(['GET'])
@permission_classes([]) # Público
def health(request):
    return JsonResponse({"status": "ok", "server": "django-iot-smartconnect"})

class InfoView(APIView):
    permission_classes = [] # Público
    def get(self, request):
        data = {
            "autor": ["Estudiante INACAP"],
            "asignatura": "Programación Back End",
            "proyecto": "Smart Barrier IoT",
            "descripcion": "Sistema de control de acceso vehicular",
            "version": "1.0"
        }
        return Response(data, status=status.HTTP_200_OK)


# ==============================================================================
# 4. VIEWSETS (CRUDs Completos)
# ==============================================================================

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAdminOrReadOnly] 

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdminOrReadOnly] 

    # PROTECCIÓN ADICIONAL MANUAL: Por si el permiso fallara
    def create(self, request, *args, **kwargs):
        if str(request.user.rol) != 'admin' and not request.user.is_superuser:
            return Response(
                {"detail": "Acción denegada. Solo los administradores pueden crear usuarios."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAdminOrReadOnly] 

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated] 
    http_method_names = ['get', 'post', 'head'] 

class ComandoRemotoViewSet(viewsets.ModelViewSet):
    queryset = ComandoRemoto.objects.all()
    serializer_class = ComandoRemotoSerializer
    permission_classes = [IsAuthenticated]


# ==============================================================================
# 5. SIMULACIÓN DE ACCESO
# ==============================================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def simular_acceso(request):
    codigo = request.data.get('codigo_sensor')
    
    if not codigo:
        return Response({
            "error": "Solicitud Incorrecta",
            "codigo": 400,
            "mensaje": "Falta el parámetro 'codigo_sensor'"
        }, status=400)

    try:
        sensor = Sensor.objects.get(codigo_sensor=codigo)
    except Sensor.DoesNotExist:
        Evento.objects.create(
            tipo_evento='ACCESO_RECHAZADO', 
            resultado='SENSOR_NO_ENCONTRADO'
        )
        return Response({
            "error": "No Encontrado",
            "codigo": 404,
            "mensaje": "Sensor no registrado en el sistema"
        }, status=404)

    if sensor.estado == 'activo':
        Evento.objects.create(
            sensor=sensor, 
            usuario=sensor.usuario, 
            tipo_evento='ACCESO_VALIDO', 
            resultado='PERMITIDO'
        )
        return Response({
            "mensaje": "Bienvenido", 
            "abrir_barrera": True,
            "usuario": str(sensor.usuario)
        }, status=200)
    else:
        Evento.objects.create(
            sensor=sensor, 
            usuario=sensor.usuario, 
            tipo_evento='ACCESO_RECHAZADO', 
            resultado=f'DENEGADO ({sensor.estado})'
        )
        return Response({
            "error": "Acceso Denegado",
            "codigo": 403,
            "mensaje": f"El sensor está {sensor.estado}",
            "abrir_barrera": False
        }, status=403)