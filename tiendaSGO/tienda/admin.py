from django.contrib import admin
from . import models


@admin.register(models.Producto)
class ProductoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Marca)
class MarcaAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Compra)
class CompraAdmin(admin.ModelAdmin):
    pass

@admin.register(models.ItemCompra)
class ItemCompraAdmin(admin.ModelAdmin):
    pass