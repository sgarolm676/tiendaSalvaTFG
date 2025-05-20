from django.db import models

class Producto(models.Model):
    COLORES_CHOICES = [
        ('Rojo', 'Rojo'),
        ('Azul', 'Azul'),
        ('Verde', 'Verde'),
        ('Negro', 'Negro'),
        ('Blanco', 'Blanco'),
        ('Gris', 'Gris'),
        ('Amarillo', 'Amarillo'),
        ('Morado', 'Morado'),
    ]

    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    unidades = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    color = models.CharField(max_length=20, choices=COLORES_CHOICES, default='Negro')

    def __str__(self):
        return f"{self.marca} - {self.modelo}"