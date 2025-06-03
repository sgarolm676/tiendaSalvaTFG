from django.shortcuts import render, get_object_or_404
from .models import Compra, ItemCompra,Producto, Perfil, DireccionEnvio, TarjetaPago, Carrito, ItemCarrito, ComentarioProducto
from .forms import RegistroUsuarioForm, PersonalizacionForm, UserUpdateForm,ComentarioProductoForm, PerfilUpdateForm, DireccionEnvioForm, TarjetaPagoForm

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest

def lista_productos(request):
    productos = Producto.objects.all().order_by('-ventas')  # Más vendidos primero
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

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    # Colores disponibles para ese modelo
    colores_disponibles = Producto.objects.filter(modelo=producto.modelo).values_list('color', flat=True).distinct()

    # Formularios
    personalizacion_form = PersonalizacionForm()
    comentario_form = ComentarioProductoForm()
    comentarios = producto.comentarios.order_by('-fecha')  # Relación related_name='comentarios'

    if request.method == 'POST':
        if 'personalizacion_submit' in request.POST:
            personalizacion_form = PersonalizacionForm(request.POST, request.FILES)
            if personalizacion_form.is_valid():
                color = personalizacion_form.cleaned_data['color']
                posicion = personalizacion_form.cleaned_data['posicion']
                tipo = personalizacion_form.cleaned_data['tipo']
                frase = personalizacion_form.cleaned_data['frase']
                imagen = personalizacion_form.cleaned_data['imagen']
                print(color, posicion, tipo, frase, imagen)
                # Aquí puedes guardar los datos si quieres

        elif 'comentario_submit' in request.POST:
            comentario_form = ComentarioProductoForm(request.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.usuario = request.user
                comentario.producto = producto
                comentario.save()
                return redirect('detalle_producto', id=producto.id)

    return render(request, 'productos/detalle_producto.html', {
        'producto': producto,
        'colores_disponibles': colores_disponibles,
        'form': personalizacion_form,
        'comentario_form': comentario_form,
        'comentarios': comentarios
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

@login_required
def configuracion_usuario(request):
    direccion, _ = DireccionEnvio.objects.get_or_create(usuario=request.user)
    tarjeta, _ = TarjetaPago.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        direccion_form = DireccionEnvioForm(request.POST, instance=direccion)
        tarjeta_form = TarjetaPagoForm(request.POST, instance=tarjeta)

        if direccion_form.is_valid() and tarjeta_form.is_valid():
            direccion_form.save()

            tarjeta = tarjeta_form.save(commit=False)
            tarjeta.usuario = request.user  # asignación automática
            tarjeta.save()

            messages.success(request, "Configuración actualizada correctamente.")
            return redirect('configuracion')

    else:
        direccion_form = DireccionEnvioForm(instance=direccion)
        tarjeta_form = TarjetaPagoForm(instance=tarjeta)

    return render(request, 'perfil/configuracion.html', {
        'direccion_form': direccion_form,
        'tarjeta_form': tarjeta_form,
        'direccion': direccion,
        'tarjeta': tarjeta,
    })

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    personalizado = request.POST.get('personalizado') == 'True'

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    ItemCarrito.objects.create(
        carrito=carrito,
        producto=producto,
        cantidad=1,
        personalizado=personalizado
    )
    return redirect('ver_carrito')  # ✅ redirige a la vista, no al template


@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    return redirect('ver_carrito')


@login_required
def ver_carrito(request):
    carrito = request.user.carrito
    context = {
        'carrito': carrito,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'carrito/ver_carrito.html', context)
@login_required
@require_POST
def aumentar_cantidad(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.cantidad += 1
    item.save()
    return redirect('ver_carrito')

@login_required
@require_POST
def disminuir_cantidad(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    return redirect('ver_carrito')

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
@csrf_exempt
def crear_checkout_session(request):
    carrito = request.user.carrito
    items = []

    # Verificar stock antes de proceder al pago
    for item in carrito.items.all():
        if item.producto.unidades < item.cantidad:
            return JsonResponse({'error': f'No hay suficiente stock para {item.producto.marca} - {item.producto.modelo}'}, status=400)

    for item in carrito.items.all():
        items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': f'{item.producto.marca} - {item.producto.modelo}',
                },
                'unit_amount': int(item.producto.precio * 100),
            },
            'quantity': item.cantidad,
        })

    if not items:
        return HttpResponseBadRequest("El carrito está vacío")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items,
            mode='payment',
            success_url=request.build_absolute_uri('/pago-exitoso/'),
            cancel_url=request.build_absolute_uri('/carrito/'),
        )
        return JsonResponse({'id': session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def procesar_pago(request):
    carrito = request.user.carrito

    if not carrito.items.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')

    # Simular que el pago fue exitoso
    # Aquí es donde normalmente usarías Stripe

    # Reducir unidades del stock
    for item in carrito.items.all():
        producto = item.producto
        producto.unidades -= item.cantidad
        producto.save()

        # Registrar venta
        producto.ventas += item.cantidad
        producto.save()

    # Vaciar el carrito
    carrito.items.all().delete()

    # Mensaje de confirmación
    messages.success(request, "✅ Pago realizado con éxito.")

    return redirect('lista_productos')


@login_required
def pago_exitoso(request):
    carrito = request.user.carrito

    if not carrito.items.exists():
        messages.error(request, "El carrito está vacío.")
        return redirect('ver_carrito')

    total = carrito.get_total_carrito()

    # Crear la compra
    compra = Compra.objects.create(usuario=request.user, total=total)

    for item in carrito.items.all():
        producto = item.producto

        # Crear item de compra
        ItemCompra.objects.create(
            compra=compra,
            producto=producto,
            cantidad=item.cantidad,
            personalizado=item.personalizado
        )

        # Actualizar producto
        producto.unidades -= item.cantidad
        producto.ventas += item.cantidad
        producto.save()

    # Vaciar carrito
    carrito.items.all().delete()

    messages.success(request, "¡Pago realizado con éxito! Tu pedido está en camino.")
    return render(request, 'carrito/pago_exitoso.html')

@login_required
def compras_anteriores(request):
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'perfil/compras_anteriores.html', {'compras': compras})

def salir(request):
    logout(request)
    return redirect('lista_productos')

