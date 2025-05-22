from django.db import models
from django.contrib.auth.models import User


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
    

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatars/', default='avatars/default.jpeg')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
    
class DireccionEnvio(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='direccionenvio')
    nombre_completo = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre_completo} ({self.usuario.username})"
    
class TarjetaPago(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tarjetapago')
    titular = models.CharField(max_length=100)
    numero = models.CharField(max_length=16)
    expiracion = models.CharField(max_length=5)  # formato MM/YY
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f"Tarjeta de {self.titular} ({self.usuario.username})"
    

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def get_total_carrito(self):
        return sum(item.get_total_item() for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    personalizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.producto.marca} ({'Personalizado' if self.personalizado else 'Normal'})"
    def get_total_item(self):
        return self.producto.precio * self.cantidad

    
    

