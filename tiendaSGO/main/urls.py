from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    #ruta para establecer idioma
    path('i18n/', include('django.conf.urls.i18n')),
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('user_configuration/', views.UserConfigurationView.as_view(), name='user_configuration'),
    path('user_configuration/user/<pk>/update', views.UpdateUserView.as_view(), name='update_user'),
    path('user_configuration/direccion/add', views.CreateDireccionView.as_view(), name='add_direccion'),
    path('user_configuration/direccion/<pk>/update', views.UpdateDireccionView.as_view(), name='update_direccion'),
    path('user_configuration/direccion/<pk>/delete', views.DeleteDireccionView.as_view(), name='delete_direccion'),
    path('user_configuration/tarjeta/add', views.CreateTarjetaView.as_view(), name='add_tarjeta'),
    path('user_configuration/tarjeta/<pk>/update', views.UpdateTarjetaView.as_view(), name='update_tarjeta'),
    path('user_configuration/tarjeta/<pk>/delete', views.DeleteTarjetaView.as_view(), name='delete_tarjeta'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/signup/', views.RegisterView.as_view(), name='signup'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('tienda/', include('tienda.urls')),
    path('captcha/', include('captcha.urls')),
]
