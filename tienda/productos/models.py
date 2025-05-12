from django.db import models

class Producto(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.marca} - {self.modelo}"