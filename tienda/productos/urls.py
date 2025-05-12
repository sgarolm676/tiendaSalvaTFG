from django.urls import path, include

from . import views
from .views import lista_productos, cerrar_sesion

urlpatterns = [
    path('', lista_productos, name='lista_productos'),
    path('register/', views.register, name='register'),
    path('registration/login', include('django.contrib.auth.urls')),
    path('logout/', cerrar_sesion, name='logout'),
]
