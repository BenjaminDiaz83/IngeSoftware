# MenuApp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plato
from .forms import PlatoForm
from django.http import JsonResponse
from django.forms import modelformset_factory
from django.contrib import messages
from .models import Plato, Ingrediente
from .forms import PlatoForm, IngredienteStockForm, IngredienteForm
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import PlatoSerializer, IngredienteSerializer

# --- Vistas API RESTful ---
class PlatoViewSet(viewsets.ModelViewSet):
    """API endpoint que permite ver o editar platos."""
    queryset = Plato.objects.all().select_related('categoria').prefetch_related('ingredientes')
    serializer_class = PlatoSerializer
    permission_classes = [AllowAny]
    
class IngredienteViewSet(viewsets.ModelViewSet):
    """API endpoint que permite ver o editar ingredientes."""
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer
    permission_classes = [AllowAny]

def listar_platos(request): 
    """Vista que recupera todos los platos y los muestra."""
    platos = Plato.objects.all().select_related('categoria').prefetch_related('ingredientes')
    
    context = {
        'platos': platos,
        'titulo': 'Menú del Restaurante'
    }
    
    return render(request, 'menu/lista_platos.html', context) 

def crear_plato(request):
    """Vista para que el Chef/Administrador cree un nuevo plato."""
    if request.method == 'POST':
        form = PlatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_platos') 
    else:
        form = PlatoForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Nuevo Plato'
    }
    return render(request, 'menu/formulario_plato.html', context)


def editar_plato(request, pk):
    """Vista para editar un plato existente (identificado por su clave primaria, pk)."""
    plato = get_object_or_404(Plato, pk=pk) 
    
    if request.method == 'POST':
        form = PlatoForm(request.POST, instance=plato)
        if form.is_valid():
            form.save()
            return redirect('lista_platos')
    else:
        form = PlatoForm(instance=plato)
    
    context = {
        'form': form,
        'titulo': f'Editar Plato: {plato.nombre}'
    }
    
    return render(request, 'menu/formulario_plato.html', context)


def eliminar_plato(request, pk):
    """Vista para eliminar un plato, requiriendo confirmación POST."""
    plato = get_object_or_404(Plato, pk=pk)
    
    if request.method == 'POST':
        plato.delete()
        return redirect('lista_platos')
        
    context = {
        'plato': plato,
        'titulo': f'Confirmar Eliminación: {plato.nombre}'
    }
    return render(request, 'menu/confirmar_eliminar.html', context)

def administrador(request):
    """
    Vista que sirve como panel central de herramientas para el Cocinero.
    Ofrece enlaces directos a Crear, Editar (a través de la lista), Eliminar, y Gestión de Stock.
    """
    context = {
        'titulo': 'Panel de Control del Chef',
    }
    return render(request, 'menu/administrador.html', context)

def stock_ingredientes(request):
    """
    Vista para gestionar el stock de todos los ingredientes.
    Muestra una tabla con el nombre del ingrediente y un campo numérico para el stock.
    """
    IngredienteFormSet = modelformset_factory(
        Ingrediente,
        form=IngredienteStockForm,
        extra=0
    )

    if request.method == 'POST':
        formset = IngredienteFormSet(request.POST, queryset=Ingrediente.objects.all())
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Stock de ingredientes actualizado correctamente.')
            return redirect('stock_ingredientes')
    else:
        formset = IngredienteFormSet(queryset=Ingrediente.objects.all())

    context = {
        'titulo': 'Gestión de Stock de Ingredientes',
        'formset': formset,
    }
    return render(request, 'menu/stock_ingredientes.html', context)

def crear_ingrediente(request):
    """
    Crea un nuevo ingrediente (nombre + stock inicial),
    luego redirige a la página de stock de ingredientes.
    """
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingrediente creado correctamente.')
            return redirect('stock_ingredientes')
    else:
        form = IngredienteForm()

    context = {
        'titulo': 'Crear nuevo ingrediente',
        'form': form,
    }
    return render(request, 'menu/formulario_ingrediente.html', context)


@require_http_methods(["POST"])
def deshabilitar_plato(request, plato_id):
    """Deshabilita un plato (plato.activo = False) y retorna éxito en JSON."""
    try:
        plato = Plato.objects.get(id=plato_id)
        plato.activo = False
        plato.save()
        return JsonResponse({'success': True, 'message': f'Plato {plato_id} deshabilitado con éxito.'})
    except Plato.DoesNotExist:
        return JsonResponse({'success': False, 'message': f'Plato ID {plato_id} no encontrado.'}, status=404)
    except Exception as e:
        # Manejo de otros errores (ej. error de base de datos)
        return JsonResponse({'success': False, 'message': f'Error interno: {str(e)}'}, status=500)

@require_http_methods(["POST"])
def habilitar_plato(request, plato_id):
    """Habilita un plato (plato.activo = True) y retorna éxito en JSON."""
    try:
        plato = Plato.objects.get(id=plato_id)
        plato.activo = True
        plato.save()
        return JsonResponse({'success': True, 'message': f'Plato {plato_id} habilitado con éxito.'})
    except Plato.DoesNotExist:
        return JsonResponse({'success': False, 'message': f'Plato ID {plato_id} no encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error interno: {str(e)}'}, status=500)