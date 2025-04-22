from django.db import models
from main.models import Cliente, Direccion, Tarjeta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

class Marca(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nombre"))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name=_("Marca")
        verbose_name_plural=_("Marcas")


class Producto(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nombre"))
    modelo = models.CharField(max_length=100, verbose_name=_("Modelo"))
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name=_("Marca"))
    unidades = models.IntegerField(verbose_name=_("Unidades"))
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Precio"))
    vip = models.BooleanField(default=False, verbose_name="VIP")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=_("Producto")
        verbose_name_plural=_("Productos")


class Valoracion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name=_("Cliente"))
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,verbose_name=_("Producto"))
    rate = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(5)], max_digits=3, decimal_places=2, verbose_name=_("Nota"))
    comentario = models.TextField(max_length=300, null=True, blank=True, verbose_name=_("Comentario"))

    def __str__(self):
        return f"{self.cliente} - {self.producto}"

    class Meta:
        verbose_name=_("Valoracion")
        verbose_name_plural=_("Valoraciones")
        constraints = [
            models.UniqueConstraint(
                fields=['cliente', 'producto'], name='unique_cliente_producto_combination'
            )
        ]


class Compra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name=_("Cliente"))
    productos = models.ManyToManyField(Producto, verbose_name=_("Productos"), through="ItemCompra")
    importe = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Importe"))
    iva = models.IntegerField(default=21, verbose_name="IVA")
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, verbose_name=_("Dirección"))
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, verbose_name=_("Tarjeta"))
    fecha = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha"))

    def __str__(self):
        return f"{self.cliente.user.username} - ({self.fecha})"

    class Meta:
        verbose_name=_("Compra")
        verbose_name_plural=_("Compras")


class ItemCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, verbose_name=_("Cliente"))
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name=_("Producto"))
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Precio"))
    unidades = models.IntegerField(verbose_name=_("Unidades"))
    
    class Meta:
        verbose_name=_("ItemCompra")
        verbose_name_plural=_("ItemCompras")
