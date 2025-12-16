from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Departamento, Sensor, Evento, ComandoRemoto

# 1. Configuración especial para el Usuario (porque usamos uno personalizado)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    # Estos son los campos que se verán en la lista del admin
    list_display = ['username', 'email', 'rol', 'departamento', 'estado', 'is_staff']
    
    # Agregamos nuestros campos personalizados al formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información Extra SmartConnect', {'fields': ('rut', 'telefono', 'rol', 'estado', 'departamento')}),
    )

# 2. Configuración para Sensores
class SensorAdmin(admin.ModelAdmin):
    list_display = ['codigo_sensor', 'tipo', 'estado', 'usuario', 'departamento']
    list_filter = ['estado', 'tipo']
    search_fields = ['codigo_sensor', 'usuario__username']

# 3. Configuración para Eventos (Historial)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['fecha_hora', 'tipo_evento', 'resultado', 'usuario', 'sensor']
    list_filter = ['tipo_evento', 'resultado']
    readonly_fields = ['fecha_hora'] # Para que nadie falsifique la fecha

# 4. Registramos todo para que aparezca
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Departamento)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(ComandoRemoto)