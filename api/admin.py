from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Departamento, Sensor, Evento, ComandoRemoto

# 1. Configuración avanzada para USUARIOS
# Heredamos de UserAdmin para mantener la gestión de contraseñas segura
class CustomUserAdmin(UserAdmin):
    model = Usuario
    
    # Columnas que se ven en la lista
    list_display = ('username', 'email', 'rol', 'estado', 'rut', 'departamento')
    
    # Filtros a la derecha
    list_filter = ('rol', 'estado', 'is_staff')
    
    # Campos para agregar al formulario de edición (para ver RUT, Rol, etc.)
    fieldsets = UserAdmin.fieldsets + (
        ('Información Extra del Proyecto', {
            'fields': ('rut', 'telefono', 'rol', 'estado', 'departamento', 'codigo_verificacion'),
        }),
    )

# 2. Configuración para DEPARTAMENTOS
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'torre', 'condominio', 'piso')
    search_fields = ('numero', 'torre')

# 3. Configuración para SENSORES
class SensorAdmin(admin.ModelAdmin):
    list_display = ('codigo_sensor', 'tipo', 'estado', 'usuario', 'fecha_alta')
    list_filter = ('estado', 'tipo')
    search_fields = ('codigo_sensor',)

# 4. Configuración para EVENTOS
class EventoAdmin(admin.ModelAdmin):
    list_display = ('fecha_hora', 'tipo_evento', 'resultado', 'sensor', 'usuario')
    list_filter = ('tipo_evento', 'resultado')
    readonly_fields = ('fecha_hora',) # Para que nadie falsee la fecha

# 5. Configuración para COMANDOS
class ComandoRemotoAdmin(admin.ModelAdmin):
    list_display = ('comando', 'dispositivo_id', 'fecha_actualizacion')
    readonly_fields = ('fecha_actualizacion',)

# --- REGISTRO DE MODELOS ---
admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(ComandoRemoto, ComandoRemotoAdmin)