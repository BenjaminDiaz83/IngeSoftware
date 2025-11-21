from django import forms
from .models import Plato, Ingrediente

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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Obtener todos los ingredientes
        ingredientes_qs = Ingrediente.objects.all()
        
        # Crear la lista de opciones (value, label) que incluye el stock en HTML
        choices = []
        for ingrediente in ingredientes_qs:
            # Creamos un label con HTML (badge de Bootstrap) para mostrar el stock
            label = f"{ingrediente.nombre} - {ingrediente.stock} restantes"
            choices.append((ingrediente.pk, label))
            
        # Asignar las nuevas opciones al campo
        self.fields['ingredientes'].choices = choices
        
        
class IngredienteStockForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['stock']
        widgets = {
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            })
        }

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Tomate'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            })
        }