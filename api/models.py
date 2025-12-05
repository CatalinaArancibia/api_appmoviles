from django.db import models
from django.contrib.auth.models import AbstractUser

# ==============================================================================
# 1. MODELO DEPARTAMENTO (Basado en tu tabla 'departamentos')
# ==============================================================================
class Departamento(models.Model):
    # En tu tabla es 'id_departamento', pero Django usa 'id' automático por defecto.
    # Mapeamos los campos exactos de tu imagen:
    numero = models.CharField(max_length=20, unique=True)  # Ej: "101-A"
    torre = models.CharField(max_length=50, null=True, blank=True)
    condominio = models.CharField(max_length=100, default="Principal")
    piso = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Depto {self.numero} (Torre {self.torre})"

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"


# ==============================================================================
# 2. MODELO USUARIO PERSONALIZADO (Basado en tu tabla 'usuarios')
# ==============================================================================
# Heredamos de AbstractUser para tener login, JWT y tokens automáticos.
class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
    )
    ESTADOS = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )

    # Campos extra que pide tu tabla 'usuarios' y no trae Django por defecto:
    rut = models.CharField(max_length=15, null=True, blank=True, unique=True)
    telefono = models.CharField(max_length=25, null=True, blank=True)
    
    # 'rol' y 'estado' son ENUMs en tu BD
    rol = models.CharField(max_length=20, choices=ROLES, default='operador')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    
    # Relación con Departamento (Clave foránea 'id_departamento')
    departamento = models.ForeignKey(
        Departamento, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='habitantes'
    )
    
    # Campos para recuperación de contraseña (según tu imagen)
    codigo_verificacion = models.CharField(max_length=10, null=True, blank=True)
    fecha_codigo = models.DateTimeField(null=True, blank=True)

    # Django ya trae: first_name (nombres), last_name (apellidos), email, password, date_joined (fecha_creacion)
    
    def __str__(self):
        return f"{self.username} ({self.rol})"


# ==============================================================================
# 3. MODELO SENSOR / RFID (Basado en tu tabla 'sensores')
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

    codigo_sensor = models.CharField(max_length=50, unique=True) # UID RFID
    estado = models.CharField(max_length=20, choices=ESTADOS_SENSOR, default='activo')
    tipo = models.CharField(max_length=20, choices=TIPOS_SENSOR, default='llavero')
    
    # Relaciones
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, related_name='sensores')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)

    # Fechas de control
    fecha_alta = models.DateTimeField(auto_now_add=True) # Se llena solo al crear
    fecha_baja = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigo_sensor} - {self.estado}"

    class Meta:
        verbose_name = "Sensor RFID"
        verbose_name_plural = "Sensores RFID"


# ==============================================================================
# 4. MODELO HISTORIAL DE ACCESO (Basado en tu tabla 'eventos_acceso')
# ==============================================================================
class Evento(models.Model):
    TIPOS_EVENTO = (
        ('ACCESO_VALIDO', 'Acceso Válido'),
        ('ACCESO_RECHAZADO', 'Acceso Rechazado'),
        ('APERTURA_MANUAL', 'Apertura Manual'),
    )

    # Relaciones opcionales (porque puede ser un sensor desconocido)
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    
    tipo_evento = models.CharField(max_length=50, choices=TIPOS_EVENTO)
    resultado = models.CharField(max_length=50) # Ej: PERMITIDO, SENSOR_BLOQUEADO
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha_hora} - {self.resultado}"

    class Meta:
        ordering = ['-fecha_hora'] # Ordenar del más reciente al más antiguo


# ==============================================================================
# 5. MODELO COMANDOS REMOTOS (Basado en tu tabla 'comandos_remotos')
# ==============================================================================
class ComandoRemoto(models.Model):
    COMANDOS = (
        ('ABRIR', 'ABRIR'),
        ('CERRAR', 'CERRAR'),
        ('NINGUNO', 'NINGUNO'),
    )

    dispositivo_id = models.CharField(max_length=50, default="BARRERA_PRINCIPAL")
    comando = models.CharField(max_length=20, choices=COMANDOS, default='NINGUNO')
    fecha_actualizacion = models.DateTimeField(auto_now=True) # Se actualiza cada vez que guardas

    def __str__(self):
        return f"{self.dispositivo_id}: {self.comando}"