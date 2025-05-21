from django.contrib import admin
from .models import Producto, DireccionEnvio, TarjetaPago, Perfil

# Register your models here.
admin.site.register(Producto)
admin.site.register(Perfil)
admin.site.register(DireccionEnvio)
admin.site.register(TarjetaPago)
