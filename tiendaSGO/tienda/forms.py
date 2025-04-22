from django import forms
from decimal import Decimal
from .models import Marca, Producto, Cliente
from main.models import Direccion, Tarjeta
from django.utils.translation import gettext_lazy as _


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"


class UnidadesForm(forms.Form):
    unidades = forms.IntegerField(initial=1, min_value=1, label=_("Unidades"))
    direccion = forms.ModelChoiceField(queryset=Direccion.objects.none(), label=_("Direccion"))
    tarjeta = forms.ModelChoiceField(queryset=Tarjeta.objects.none(), label=_("Tarjeta"))
    
    def __init__(self, *args, **kwargs):
        self.cliente = kwargs.pop("cliente", None)
        self.producto = kwargs.pop("producto", None)
        super().__init__(*args, **kwargs)
        self.fields["direccion"].queryset = Direccion.objects.filter(cliente=self.cliente)
        self.fields["tarjeta"].queryset = Tarjeta.objects.filter(cliente=self.cliente)

    def clean_unidades(self):
        unidades = self.cleaned_data["unidades"]
        if unidades > self.producto.unidades:
            raise forms.ValidationError(_("No hay suficientes existencias!"))
        elif unidades * self.producto.precio > self.cliente.saldo:
            raise forms.ValidationError(_("No tienes suficiente dinero! Te faltan") + " " + str(unidades * self.producto.precio - self.cliente.saldo))
        return unidades


class CarritoForm(forms.Form):
    direccion = forms.ModelChoiceField(queryset=Direccion.objects.none(), label=_("Direccion"))
    tarjeta = forms.ModelChoiceField(queryset=Tarjeta.objects.none(), label=_("Tarjeta"))
    
    def __init__(self, *args, **kwargs):
        self.cliente = kwargs.pop("cliente", None)
        self.carrito = kwargs.pop("carrito", None)
        super().__init__(*args, **kwargs)
        self.fields["direccion"].queryset = Direccion.objects.filter(cliente=self.cliente)
        self.fields["tarjeta"].queryset = Tarjeta.objects.filter(cliente=self.cliente)

    def clean(self):
        precio_total = 0
        for c in self.carrito:
            if c.cantidad > c.producto.unidades:
                error = forms.ValidationError(_("No hay suficientes existencias del producto") + f" {c.producto.name}")
                self.add_error("tarjeta", error)
                raise error
            precio_total += c.producto.precio * c.cantidad
        if precio_total > self.cliente.saldo:
            error = forms.ValidationError(_("No tienes suficiente dinero! Te faltan") + " " + str(precio_total - Decimal(self.cliente.saldo)))
            self.add_error("tarjeta", error)
            raise error
