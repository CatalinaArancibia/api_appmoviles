from django.db import models
from django.contrib.auth.models import AbstractUser

# ==============================================================================
# 1. MODELO DEPARTAMENTO (Tabla 'departamentos')
# ==============================================================================
class Departamento(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    torre = models.CharField(max_length=50, null=True, blank=True)
    condominio = models.CharField(max_length=100, default="Principal")
    piso = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Depto {self.numero} (Torre {self.torre})"

    class Meta:
        # IMPORTANTE: Si tu tabla en MySQL se llama 'departamentos', pon esto:
        db_table = 'departamentos'  
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"


# ==============================================================================
# 2. MODELO USUARIO (Tabla 'usuarios')
# ==============================================================================
class Usuario(AbstractUser):
    # --- A. Reemplazo de campos de Django por los tuyos ---
    
    # 1. NOMBRES Y APELLIDOS
    first_name = None  # Borramos el de Django
    last_name = None   # Borramos el de Django
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")

    # 2. EMAIL (El truco maestro)
    # Llamamos a la variable 'email' (para que Django Auth funcione feliz),
    # pero le decimos que lea la columna 'correo' de tu base de datos.
    email = models.EmailField(unique=True, db_column='correo', verbose_name="Correo") 

    # 3. FECHA CREACIÓN
    # Django usa 'date_joined'. Hacemos que apunte a tu columna 'fecha_creacion'.
    date_joined = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    # --- B. Campos propios de tu tabla ---
    rut = models.CharField(max_length=15, null=True, blank=True, unique=True)
    telefono = models.CharField(max_length=25, null=True, blank=True)
    
    ROLES = (('admin', 'Administrador'), ('operador', 'Operador'))
    rol = models.CharField(max_length=20, choices=ROLES, default='operador')
    
    ESTADOS = (('activo', 'Activo'), ('inactivo', 'Inactivo'))
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    
    # FK apuntando a la columna 'id_departamento'
    departamento = models.ForeignKey(
        Departamento, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='id_departamento', 
        related_name='habitantes'
    )
    
    codigo_verificacion = models.CharField(max_length=10, null=True, blank=True)
    fecha_codigo = models.DateTimeField(null=True, blank=True)

    # --- C. Configuración de Login ---
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email', 'nombres', 'apellidos'] # Usamos 'email' aquí también

    def __str__(self):
        return f"{self.username} ({self.rol})"

    class Meta:
        db_table = 'usuarios' # Tu tabla existente


# ==============================================================================
# 3. MODELO SENSOR (Tabla 'sensores')
# ==============================================================================
class Sensor(models.Model):
    ESTADOS_SENSOR = (
        ('activo', 'Activo'), ('inactivo', 'Inactivo'),
        ('perdido', 'Perdido'), ('bloqueado', 'Bloqueado'),
    )
    TIPOS_SENSOR = (('llavero', 'Llavero'), ('tarjeta', 'Tarjeta'))

    codigo_sensor = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_SENSOR, default='activo')
    tipo = models.CharField(max_length=20, choices=TIPOS_SENSOR, default='llavero')
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, related_name='sensores')
    # Si en sensores la columna es 'id_departamento', agrega db_column='id_departamento' aquí abajo
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)

    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigo_sensor} - {self.estado}"

    class Meta:
        db_table = 'sensores' # Aseguramos que lea la tabla correcta
        verbose_name = "Sensor RFID"


# ==============================================================================
# 4. MODELO EVENTO (Tabla 'eventos_acceso' o similar)
# ==============================================================================
class Evento(models.Model):
    TIPOS_EVENTO = (('ACCESO_VALIDO', 'Acceso Válido'), ('ACCESO_RECHAZADO', 'Acceso Rechazado'), ('APERTURA_MANUAL', 'Apertura Manual'))

    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    
    tipo_evento = models.CharField(max_length=50, choices=TIPOS_EVENTO)
    resultado = models.CharField(max_length=50)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'eventos_acceso' # Ajusta si tu tabla se llama diferente
        ordering = ['-fecha_hora']


# ==============================================================================
# 5. MODELO COMANDO (Tabla 'comandos_remotos')
# ==============================================================================
class ComandoRemoto(models.Model):
    COMANDOS = (('ABRIR', 'ABRIR'), ('CERRAR', 'CERRAR'), ('NINGUNO', 'NINGUNO'))

    dispositivo_id = models.CharField(max_length=50, default="BARRERA_PRINCIPAL")
    comando = models.CharField(max_length=20, choices=COMANDOS, default='NINGUNO')
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comandos_remotos' # Ajusta nombre