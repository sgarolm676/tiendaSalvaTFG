from django.shortcuts import render, get_object_or_404
from .models import Producto
from .forms import RegistroUsuarioForm, PersonalizacionForm, UserUpdateForm, PerfilUpdateForm

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {'productos': productos})

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # login automático
            return redirect('lista_productos')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'productos/register.html', {'form': form})

@require_POST
@csrf_protect
def cerrar_sesion(request):
    logout(request)
    return redirect('lista_productos')  # O la vista principal que desees

@login_required
def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    # Obtener todos los colores disponibles para el mismo modelo, sin repetidos
    colores_disponibles = Producto.objects.filter(modelo=producto.modelo).values_list('color', flat=True).distinct()

    if request.method == 'POST':
        form = PersonalizacionForm(request.POST, request.FILES)
        if form.is_valid():
            color = form.cleaned_data['color']
            posicion = form.cleaned_data['posicion']
            tipo = form.cleaned_data['tipo']
            frase = form.cleaned_data['frase']
            imagen = form.cleaned_data['imagen']
            print(color, posicion, tipo, frase, imagen)
            # Aquí puedes añadir más lógica según necesites

    else:
        form = PersonalizacionForm()

    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'form': form,
        'colores_disponibles': colores_disponibles,
    })

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        perfil_form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('lista_productos')  # redirige a lista de productos
    else:
        user_form = UserUpdateForm(instance=request.user)
        perfil_form = PerfilUpdateForm(instance=request.user.perfil)

    context = {
        'user_form': user_form,
        'perfil_form': perfil_form
    }
    return render(request, 'perfil/editar_perfil.html', context)