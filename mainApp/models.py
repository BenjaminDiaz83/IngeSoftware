from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorias"

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class Plato(models.Model):
    """Corresponde a la tabla Menu en el diagrama de clases."""
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    imagen = models.ImageField(upload_to='platos/', null=True, blank=True)

    activo = models.BooleanField(default=True)
    
    # Relaciones
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    ingredientes = models.ManyToManyField(Ingrediente, related_name='platos')
    
    class Meta:
        ordering = ['categoria', 'nombre']
        verbose_name_plural = "Platos"

    def __str__(self):
        return self.nombre
    
    def tiene_stock_suficiente(self):
        ingredientes = self.ingredientes.all()
        if not ingredientes:
            return True
        return all(ing.stock > 0 for ing in ingredientes)