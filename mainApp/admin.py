from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Categoria, Ingrediente, Plato

class PlatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria','vista_plato') 
    list_filter = ('categoria',)
    search_fields = ('nombre', 'descripcion',)
    # Usamos filter_horizontal para seleccionar ingredientes
    filter_horizontal = ('ingredientes',) 

    def vista_plato(self, obj):
        if obj.imagen:
            return format_html ('<img src="{}" width="100" height="100" />',obj.imagen.url)
        return "No Image"

admin.site.register(Categoria)


admin.site.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'stock')
    search_fields = ('nombre',)
    actions = ['agregar_1', 'consumir_1']

    def _adjust(self, request, queryset, delta: int):
        actualizados = 0
        omitidos = 0
        for ing in queryset:
            nuevo = (ing.stock or 0) + delta
            if nuevo < 0:
                omitidos += 1
                continue
            ing.stock = nuevo
            ing.save(update_fields=['stock'])
            actualizados += 1

        if actualizados:
            messages.success(request, f"Se actualizaron {actualizados} ingrediente(s).")
        if omitidos:
            messages.warning(request, f"{omitidos} ingrediente(s) omitido(s) (no se puede dejar stock negativo).")

    def agregar_1(self, request, queryset):
        """➕ Agregar 1 unidad"""
        self._adjust(request, queryset, +1)
    agregar_1.short_description = "➕ Agregar 1"

    def consumir_1(self, request, queryset):
        """➖ Consumir 1 unidad"""
        self._adjust(request, queryset, -1)
    consumir_1.short_description = "➖ Consumir 1"



admin.site.register(Plato, PlatoAdmin)
