from rest_framework import serializers
from .models import Usuario, Departamento, Sensor, Evento, ComandoRemoto

# 1. Serializador de DEPARTAMENTOS
class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

# 2. Serializador de USUARIOS
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Listamos los campos que queremos ver en el JSON
        fields = ['id', 'username', 'password', 'nombres', 'apellidos', 'email', 'rut', 'rol', 'estado', 'departamento']
        
        # SEGURIDAD Y VALIDACIONES
        extra_kwargs = {
            'password': {'write_only': True},
            'rol': {'required': True}  # <--- ESTO OBLIGA A ENVIAR EL ROL
        }

    # Esto es necesario para encriptar la contraseña al crear un usuario desde la API
    def create(self, validated_data):
        # Usamos el método create_user que maneja la encriptación y los campos extra
        user = Usuario.objects.create_user(**validated_data)
        return user

# 3. Serializador de SENSORES
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

# 4. Serializador de EVENTOS
class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

# 5. Serializador de COMANDOS REMOTOS
class ComandoRemotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComandoRemoto
        fields = '__all__'