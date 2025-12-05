from django.http import JsonResponse
from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

def health(request):
    return JsonResponse({"status": "ok"})

def info(request):
    data = {
        "proyecto": "EcoEnergy",
        "version": "1.0",
        "autor": "Catalina Arancibia"
    }
    return JsonResponse(data)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]