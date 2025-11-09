from django.contrib import admin

from .models import Categoria, Ingrediente, Plato

class PlatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria',) 
    list_filter = ('categoria',)
    search_fields = ('nombre', 'descripcion',)
    # Usamos filter_horizontal para seleccionar ingredientes
    filter_horizontal = ('ingredientes',) 

admin.site.register(Categoria)
admin.site.register(Ingrediente)
admin.site.register(Plato, PlatoAdmin)
