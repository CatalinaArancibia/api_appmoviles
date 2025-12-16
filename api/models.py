from django.db import models
from django.contrib.auth.models import AbstractUser

# ==============================================================================
# 1. MODELO DEPARTAMENTO
# ==============================================================================
class Departamento(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    torre = models.CharField(max_length=50, null=True, blank=True)
    condominio = models.CharField(max_length=100, default="Principal")
    piso = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Depto {self.numero} (Torre {self.torre})"

# ==============================================================================
# 2. MODELO USUARIO PERSONALIZADO
# ==============================================================================
class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
    )
    ESTADOS = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )

    rut = models.CharField(max_length=15, null=True, blank=True, unique=True)
    telefono = models.CharField(max_length=25, null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='operador')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    
    departamento = models.ForeignKey(
        Departamento, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='habitantes'
    )
    
    codigo_verificacion = models.CharField(max_length=10, null=True, blank=True)
    fecha_codigo = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"

# ==============================================================================
# 3. MODELO SENSOR / RFID
# ==============================================================================
class Sensor(models.Model):
    ESTADOS_SENSOR = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('perdido', 'Perdido'),
        ('bloqueado', 'Bloqueado'),
    )
    TIPOS_SENSOR = (
        ('llavero', 'Llavero'),
        ('tarjeta', 'Tarjeta'),
    )

    codigo_sensor = models.CharField(max_length=50, unique=True) 
    estado = models.CharField(max_length=20, choices=ESTADOS_SENSOR, default='activo')
    tipo = models.CharField(max_length=20, choices=TIPOS_SENSOR, default='llavero')
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, related_name='sensores')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)

    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigo_sensor} - {self.estado}"

# ==============================================================================
# 4. MODELO HISTORIAL DE ACCESO
# ==============================================================================
class Evento(models.Model):
    TIPOS_EVENTO = (
        ('ACCESO_VALIDO', 'Acceso Válido'),
        ('ACCESO_RECHAZADO', 'Acceso Rechazado'),
        ('APERTURA_MANUAL', 'Apertura Manual'),
    )

    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    
    tipo_evento = models.CharField(max_length=50, choices=TIPOS_EVENTO)
    resultado = models.CharField(max_length=50)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha_hora} - {self.resultado}"

    class Meta:
        ordering = ['-fecha_hora']

# ==============================================================================
# 5. MODELO COMANDOS REMOTOS
# ==============================================================================
class ComandoRemoto(models.Model):
    COMANDOS = (
        ('ABRIR', 'ABRIR'),
        ('CERRAR', 'CERRAR'),
        ('NINGUNO', 'NINGUNO'),
    )

    dispositivo_id = models.CharField(max_length=50, default="BARRERA_PRINCIPAL")
    comando = models.CharField(max_length=20, choices=COMANDOS, default='NINGUNO')
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dispositivo_id}: {self.comando}"