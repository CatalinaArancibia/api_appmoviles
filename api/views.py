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
# 1. PERMISOS PERSONALIZADOS (ADMIN vs OPERADOR) -> Cumple punto 7 Rúbrica
# ==============================================================================
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado:
    - Admin: Puede hacer TODO (Crear, Leer, Actualizar, Borrar).
    - Operador/Usuario: Solo puede LEER (GET).
    """
    def has_permission(self, request, view):
        # Si el usuario no está autenticado, denegar siempre
        if not request.user or not request.user.is_authenticated:
            return False

        # Si es una petición segura (GET, HEAD, OPTIONS), permitir a cualquiera autenticado
        if request.method in permissions.SAFE_METHODS:
            return True

        # Para escribir (POST, PUT, DELETE), solo permitir si es ADMIN
        return request.user.rol == 'admin' or request.user.is_superuser


# ==============================================================================
# 2. MANEJADORES DE ERROR GLOBALES (404 Rutas y 500) -> Cumple punto 9 Rúbrica
# ==============================================================================
# Estos se activan desde ecoapi/urls.py
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
    permission_classes = [] # Público para cumplir rúbrica
    def get(self, request):
        data = {
            "autor": ["Tu Nombre Aquí"],
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
    permission_classes = [IsAdminOrReadOnly] # Solo admin edita

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAdminOrReadOnly] # Solo admin edita

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAdminOrReadOnly] # Solo admin edita

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    # Aquí cambiamos un poco: Nadie debería editar el historial, solo leer y crear
    permission_classes = [IsAuthenticated] 
    http_method_names = ['get', 'post', 'head'] # Bloqueamos PUT y DELETE para proteger historial

class ComandoRemotoViewSet(viewsets.ModelViewSet):
    queryset = ComandoRemoto.objects.all()
    serializer_class = ComandoRemotoSerializer
    permission_classes = [IsAuthenticated]


# ==============================================================================
# 5. SIMULACIÓN DE ACCESO (Lógica de Negocio)
# ==============================================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def simular_acceso(request):
    """
    Simula el paso de una tarjeta RFID.
    Maneja errores 400 (Validación), 404 (Objeto no encontrado) y 403 (Lógica negocio).
    """
    codigo = request.data.get('codigo_sensor')
    
    # Error 400: Validación
    if not codigo:
        return Response({
            "error": "Solicitud Incorrecta",
            "codigo": 400,
            "mensaje": "Falta el parámetro 'codigo_sensor'"
        }, status=400)

    try:
        sensor = Sensor.objects.get(codigo_sensor=codigo)
    except Sensor.DoesNotExist:
        # Registramos el intento fallido
        Evento.objects.create(
            tipo_evento='ACCESO_RECHAZADO', 
            resultado='SENSOR_NO_ENCONTRADO'
        )
        # Error 404: Objeto no encontrado (lógica de negocio)
        return Response({
            "error": "No Encontrado",
            "codigo": 404,
            "mensaje": "Sensor no registrado en el sistema"
        }, status=404)

    # Lógica de validación de estado
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
        # Error 403: Prohibido (por estado del sensor)
        return Response({
            "error": "Acceso Denegado",
            "codigo": 403,
            "mensaje": f"El sensor está {sensor.estado}",
            "abrir_barrera": False
        }, status=403)