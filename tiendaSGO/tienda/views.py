from typing import Any
from django.shortcuts import render, reverse, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView, View, DetailView
from django.db.models import Sum
from django.http import HttpRequest, HttpResponseBadRequest
from decimal import Decimal

from .forms import FiltrarProductos, UnidadesForm, FiltrarMarcas, FiltrarCompras, CarritoForm
from .models import Cliente, Producto, Compra, ItemCompra, Valoracion

################### Vistas del proceso de compra normal (Listado y confirmacion, donde aparecen las valoraciones) ###################
class ComprarView(ListView):
    """
    Vista del listado de todos los producto, todos los usuarios pueden acceder.
    
    Usa ListView usando como model Producto. Adicionalmente modificamos el
    get_context_data para aplicar un filtrado enviado como formulario.
    """
    template_name = "tienda/compra.html"
    model = Producto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = FiltrarProductos(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            marcas = form.cleaned_data["marca"]
            object_list = context["object_list"]
            if name:
                object_list = object_list.filter(name__icontains=name)
            if marcas:
                object_list = object_list.filter(marca__in=marcas)
            context["object_list"] = object_list
        context["form"] = form
        return context

    """
    Vista para la confirmacion y seleccion de unidades de un producto.
    Es una vista un poco especial ya que tenemos que añadir el producto y las valoraciones al
    contexto. Adicionalmente incluimos un booleano donde especificamos si el usuario puede
    o no añadir una valoracion.
    Si el usuario puede editar/borrar un producto se decide en el template usando el usuario y sus permisos.
    """
    template_name = "tienda/checkout.html"
    form_class = UnidadesForm

    def get_form_kwargs(self):
        producto = Producto.objects.get(id=self.kwargs["id"])
        cliente = Cliente.objects.get(user=self.request.user)
        kwargs = super().get_form_kwargs()
        kwargs['producto'] = producto
        kwargs['cliente'] = cliente
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto = Producto.objects.get(id=self.kwargs["id"])
        context["can_add_rate"] = not Valoracion.objects.filter(cliente=Cliente.objects.get(user=self.request.user), producto=producto).exists()
        context['producto'] = producto
        context["valoraciones"] = Valoracion.objects.filter(producto=producto)
        return context

    def form_valid(self, form):
        if form.is_valid():
            producto = form.producto
            cliente = form.cliente

            new_compra = Compra()
            new_compra.cliente = cliente
            new_compra.importe = form.cleaned_data["unidades"] * producto.precio
            new_compra.direccion = form.cleaned_data["direccion"]
            new_compra.tarjeta = form.cleaned_data["tarjeta"]
            new_compra.save()
            new_compra.productos.add(producto, through_defaults={"unidades": form.cleaned_data["unidades"], "precio": producto.precio})
            producto.unidades = producto.unidades - form.cleaned_data["unidades"]
            producto.save()

            cliente.saldo = cliente.saldo - new_compra.importe
            cliente.save()
            return super().form_valid(form)
        return render(self.request, "tienda/checkout.html", context={"form": form, "producto": producto})

    def get_success_url(self):
        return reverse("compra")
#####################################################################################################

################### Vistas del carrito ###################
class ItemCarrito:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad


def deserialize_carrito(carrito):
    return [ItemCarrito(Producto.objects.get(pk=k), int(v)) for k, v in carrito.items()]


class CarritoView(View):
    http_method_names = ['get', 'post', 'delete']

    def get(self, request):
        return render(self.request, "tienda/carrito.html", context={"carrito": deserialize_carrito(request.session.get("carrito", {}))})

    def post(self, request, pk):
        item = pk
        carrito = request.session.setdefault("carrito", {})
        if item in carrito:
            carrito[item] += 1
        else:
            carrito[item] = 1
        request.session["carrito"] = carrito
        next_url = self.request.POST.get('next', 'welcome')
        return redirect(next_url)

    template_name = "tienda/carrito_checkout.html"
    form_class = CarritoForm

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.cliente = Cliente.objects.get(user=request.user)
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrito = deserialize_carrito(self.request.session.get("carrito", {}))
        context["carrito"] = carrito
        context["precio_total"] = sum([c.producto.precio * c.cantidad for c in carrito])
        return context

    def get_form_kwargs(self):
        carrito = deserialize_carrito(self.request.session.get("carrito", {}))
        kwargs = super().get_form_kwargs()
        kwargs['carrito'] = carrito
        kwargs['cliente'] = self.cliente
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            carrito = form.carrito
            precio_total = sum([c.producto.precio * c.cantidad for c in carrito])
            compra = Compra()
            compra.cliente = self.cliente
            compra.importe = precio_total
            compra.direccion = form.cleaned_data["direccion"]
            compra.tarjeta = form.cleaned_data["tarjeta"]
            compra.iva = 0.21
            compra.save()
            for item in carrito:
                compra.productos.add(item.producto, through_defaults={"unidades": item.cantidad, "precio": item.producto.precio})
                item.producto.unidades -= item.cantidad
                print(item.producto.unidades)
                item.producto.save()
            compra.save()
            self.cliente.saldo -= Decimal(precio_total)
            self.cliente.save()
            self.request.session["carrito"] = {}
            return super().form_valid(form)
        return render(self.request, "tienda/checkout.html", context={"form": form})
    
    def get_success_url(self):
        return reverse("compra")
        

class UpdateCarritoView(View):
    def post(self, request, pk):
        item = pk
        carrito = request.session.setdefault("carrito", {})
        if int(self.request.POST.get('cantidad', 0)) > 0:
            carrito[item] = self.request.POST.get('cantidad', carrito[item])
            request.session["carrito"] = carrito
        next_url = self.request.POST.get('next', 'welcome')
        return redirect(next_url)


class RemoveCarritoView(View):
    def post(self, request, pk):
        item = pk
        carrito = request.session.setdefault("carrito", {})
        carrito.pop(item)
        request.session["carrito"] = carrito
        next_url = self.request.POST.get('next', 'welcome')
        return redirect(next_url)

#####################################################################################################


################### Vistas de los informes ###################

class CompraDetail(DetailView):
    model = Compra
    template_name = "informe/compra_detail.html"

#####################################################################################################
