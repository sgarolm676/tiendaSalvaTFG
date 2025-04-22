from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Cliente)
class ClienteAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Direccion)
class DireccionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tarjeta)
class TarjetasAdmin(admin.ModelAdmin):
    pass