from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinLengthValidator, MaxLengthValidator
from creditcards.models import CardExpiryField, SecurityCodeField
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Cliente(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("Usuario"))
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Saldo"))
    vip = models.BooleanField(default=False, verbose_name=_("VIP"))
    
    def __str__(self):
        verbose_name=_("Cliente")
        verbose_plural_name=_("Clientes")
        return f"{self.user}"
    
    class Meta:
        verbose_name=_("Cliente")
        verbose_name_plural=_("Clientes")


class Direccion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name=_("Cliente"))
    nombre = models.CharField(max_length=100, verbose_name=_("Nombre"))
    telefono_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    numero_de_telefono = models.CharField(validators=[telefono_regex], max_length=17, blank=True, verbose_name=_("Numero de telefono"))
    linea_de_direccion = models.CharField(max_length=150, verbose_name=_("Línea de dirección"))
    codigo_postal = models.PositiveIntegerField(validators=[MaxValueValidator(99999)],verbose_name=_("Código postal"))
    ciudad = models.CharField(max_length=30, verbose_name=_("Ciudad"))
    provincia = models.CharField(max_length=30, verbose_name=_("Provincia"))
    instrucciones= models.TextField(null=True, blank=True, verbose_name=_("Instrucciones"))

    def __str__(self):
        return self.linea_de_direccion
    
    class Meta:
        verbose_name = _("Direccion")
        verbose_name_plural = _("Direcciones")


class Tarjeta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name=_("Cliente"))
    titular = models.CharField(max_length=100, verbose_name=_("Titular"))
    cc_number = models.CharField(validators=[MinLengthValidator(12), MaxLengthValidator(19)], verbose_name=_("Número de tarjeta"))
    cc_expiry = CardExpiryField(verbose_name=_("Fecha de expiración"))
    cc_code = SecurityCodeField(verbose_name='CVV/CVC')

    def __str__(self):
        return f"**** **** **** {self.cc_number[-4:]}"
    
    class Meta:
        verbose_name = _("Tarjeta")
        verbose_name_plural = _("Tarjetas")
