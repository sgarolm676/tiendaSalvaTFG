from django.shortcuts import render
from .models import Producto
from .forms import RegistroUsuarioForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth import login


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