from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Perfil, DireccionEnvio, TarjetaPago, Carrito

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()

@receiver(post_save, sender=User)
def crear_perfil_configuracion(sender, instance, created, **kwargs):
    if created:
        DireccionEnvio.objects.create(usuario=instance)
        TarjetaPago.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def crear_carrito_usuario(sender, instance, created, **kwargs):
    if created:
        Carrito.objects.create(usuario=instance)
