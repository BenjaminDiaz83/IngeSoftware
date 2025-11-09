from django import forms
from .models import Plato

class PlatoForm(forms.ModelForm):
    """
    Formulario basado en el modelo Plato para la creación y edición.
    Se añade la clase 'form-control'/'form-select' a los widgets para el estilo Bootstrap.
    """
    class Meta:
        model = Plato
        # Incluimos todos los campos que el Chef necesita especificar
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'ingredientes']
        
        # Personalizar widgets y añadir clases de Bootstrap
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Lomo Saltado'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            # 💡 CLAVE 1: Usar 'form-select' y CLAVE 2: Añadir 'size' para que sea visible
            'ingredientes': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 8}),
            
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            
            # El campo 'categoria' debe usar 'form-select'
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }