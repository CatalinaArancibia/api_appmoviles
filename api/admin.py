from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Departamento, Sensor, Evento, ComandoRemoto


# ======================================================================
# ADMIN USUARIO PERSONALIZADO
# ======================================================================
class UsuarioAdmin(UserAdmin):
    model = Usuario

    # 🔒 EXCLUIMOS date_joined (campo no editable de AbstractUser)
    exclude = ('date_joined',)

    # Columnas en la lista
    list_display = (
        'username',
        'email',
        'rol',
        'departamento',
        'estado',
        'is_staff',
        'is_superuser',
    )

    list_filter = (
        'rol',
        'estado',
        'is_staff',
        'is_superuser',
        'groups',
    )

    search_fields = (
        'username',
        'email',
        'rut',
    )

    ordering = ('username',)

    # =======================
    # FORMULARIO DE EDICIÓN
    # =======================
    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
            )
        }),
        ('Información personal', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'rut',
                'telefono',
                'departamento',
            )
        }),
        ('Información SmartConnect', {
            'fields': (
                'rol',
                'estado',
                'codigo_verificacion',
            )
        }),
        ('Permisos', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
    )

    # =======================
    # FORMULARIO DE CREACIÓN
    # =======================
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'email',
                'rol',
                'estado',
                'rut',
                'telefono',
                'departamento',
            ),
        }),
    )


# ======================================================================
# ADMIN DEPARTAMENTO
# ======================================================================
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'torre', 'condominio', 'piso')
    search_fields = ('numero', 'torre', 'condominio')
    list_filter = ('condominio',)


# ======================================================================
# ADMIN SENSOR RFID
# ======================================================================
class SensorAdmin(admin.ModelAdmin):
    list_display = (
        'codigo_sensor',
        'tipo',
        'estado',
        'usuario',
        'departamento',
        'fecha_alta',
    )
    list_filter = ('estado', 'tipo')
    search_fields = ('codigo_sensor', 'usuario__username')


# ======================================================================
# ADMIN EVENTOS (HISTORIAL)
# ======================================================================
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_hora',
        'tipo_evento',
        'resultado',
        'usuario',
        'sensor',
    )
    list_filter = ('tipo_evento', 'resultado')
    readonly_fields = ('fecha_hora',)


# ======================================================================
# ADMIN COMANDOS REMOTOS
# ======================================================================
class ComandoRemotoAdmin(admin.ModelAdmin):
    list_display = (
        'dispositivo_id',
        'comando',
        'fecha_actualizacion',
    )
    list_filter = ('comando',)


# ======================================================================
# REGISTRO DE MODELOS
# ======================================================================
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(ComandoRemoto, ComandoRemotoAdmin)
