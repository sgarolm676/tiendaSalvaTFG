from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('productos.urls')),
    path('registration/login', include('django.contrib.auth.urls')),
]
