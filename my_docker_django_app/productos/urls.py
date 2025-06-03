from django.urls import path, include

from .views import compras_anteriores,salir, lista_productos, cerrar_sesion, pago_exitoso,registrar_usuario, detalle_producto,editar_perfil, configuracion_usuario, agregar_al_carrito, ver_carrito, eliminar_del_carrito, aumentar_cantidad, disminuir_cantidad, crear_checkout_session, procesar_pago
urlpatterns = [
    path('', lista_productos, name='lista_productos'),
    path('register/', registrar_usuario, name='register'),
    path('login', include('django.contrib.auth.urls')),
    path('logout/', cerrar_sesion, name='logout'),
    path('productos/<int:id>/', detalle_producto, name='detalle_producto'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    path('configuracion/', configuracion_usuario, name='configuracion'),
    path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:item_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('crear-checkout-session/', crear_checkout_session, name='crear_checkout_session'),
    path('carrito/aumentar/<int:item_id>/', aumentar_cantidad, name='aumentar_cantidad'),
    path('carrito/disminuir/<int:item_id>/', disminuir_cantidad, name='disminuir_cantidad'),
    path('pagar/', procesar_pago, name='procesar_pago'),
    path('pago-exitoso/', pago_exitoso, name='pago_exitoso'),
    path('salir/', salir, name='salir'),
    path('perfil/compras/', compras_anteriores, name='compras_anteriores'),




]
