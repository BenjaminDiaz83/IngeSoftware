# mainApp/serializers.py (¡ARCHIVO NUEVO!)

from rest_framework import serializers
from .models import Plato, Ingrediente, Categoria

# --- Serializador de Stock ---
class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ['id', 'nombre', 'stock'] 

# --- Serializador de Menú ---
class PlatoSerializer(serializers.ModelSerializer):
    # 1. Campo de lectura: Muestra los ingredientes completos (para el GET)
    ingredientes = IngredienteSerializer(many=True, read_only=True)
    
    # 2. Campo de escritura: Permite al cliente enviar una lista de IDs (para el POST/PUT)
    ingredientes_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Ingrediente.objects.all(), 
        write_only=True, 
        source='ingredientes' 
    )
    
    class Meta:
        model = Plato
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 'imagen', 
            'categoria', # El cliente enviará el ID de la Categoría
            'ingredientes', 
            'ingredientes_ids'
        ]
        read_only_fields = ['imagen'] # Las imágenes se manejan por separado