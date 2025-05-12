from django.urls import path, include

from . import views
from .views import lista_productos, cerrar_sesion, registrar_usuario

urlpatterns = [
    path('', lista_productos, name='lista_productos'),
    path('register/', registrar_usuario, name='register'),
    path('registration/login', include('django.contrib.auth.urls')),
    path('logout/', cerrar_sesion, name='logout'),
]
