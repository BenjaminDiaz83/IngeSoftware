from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorias"

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class Plato(models.Model):
    """Corresponde a la tabla Menu en tu diagrama de clases."""
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    
    # Relaciones
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    ingredientes = models.ManyToManyField(Ingrediente, related_name='platos')
    
    class Meta:
        ordering = ['categoria', 'nombre']
        verbose_name_plural = "Platos"

    def __str__(self):
        return self.nombre