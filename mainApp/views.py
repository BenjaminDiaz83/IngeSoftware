# MenuApp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plato
from .forms import PlatoForm

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