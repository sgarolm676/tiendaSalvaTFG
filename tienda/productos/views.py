from django.shortcuts import render
from .models import Producto
from .forms import RegistroForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {'productos': productos})

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}!')
            return redirect('lista_productos')  # Redirige a donde quieras
    else:
        form = RegistroForm()
    return render(request, 'productos/register.html', {'form': form})

@require_POST
@csrf_protect
def cerrar_sesion(request):
    logout(request)
    return redirect('lista_productos')  # O la vista principal que desees