# MenuApp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plato
from .forms import PlatoForm
from django.forms import modelformset_factory
from django.contrib import messages
from .models import Plato, Ingrediente
from .forms import PlatoForm, IngredienteStockForm, IngredienteForm

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
