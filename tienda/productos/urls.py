from django.urls import path, include

from . import views
from .views import lista_productos, cerrar_sesion, registrar_usuario, detalle_producto, editar_perfil, configuracion_usuario

urlpatterns = [
    path('', lista_productos, name='lista_productos'),
    path('register/', registrar_usuario, name='register'),
    path('login', include('django.contrib.auth.urls')),
    path('logout/', cerrar_sesion, name='logout'),
    path('productos/<int:id>/', detalle_producto, name='detalle_producto'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
     path('configuracion/', configuracion_usuario, name='configuracion'),
]
