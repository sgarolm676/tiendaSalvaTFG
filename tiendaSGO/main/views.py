from typing import Any
from django.shortcuts import render, reverse
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, FormView, RedirectView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Cliente, Direccion, Tarjeta
from .forms import LoginForm
# Create your views here.

######################## Template views ########################
class WelcomeView(TemplateView):
    template_name = "main/index.html"


class UserConfigurationView(TemplateView, LoginRequiredMixin):
    template_name = "main/user_config.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = Cliente.objects.get(user=self.request.user)
        context['cliente'] = cliente
        context['direcciones'] = Direccion.objects.filter(cliente=cliente)
        context['tarjetas'] = Tarjeta.objects.filter(cliente=cliente)
        return context
##############################################################

######################## User views ########################
class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ["first_name", "last_name", "email"]
    template_name = "main/user_update_form.html"
    
    def get_success_url(self):
        return reverse("user_configuration")


class CreateDireccionView(LoginRequiredMixin, CreateView):
    model = Direccion
    fields = ["nombre", "numero_de_telefono", "linea_de_direccion", "codigo_postal", "ciudad", "provincia", "instrucciones"]
    template_name_suffix = "_add_form"
    
    def form_valid(self, form):
        form.instance.cliente = Cliente.objects.get(user=self.request.user)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("user_configuration")


class UpdateDireccionView(LoginRequiredMixin, UpdateView):
    model = Direccion
    fields = ["nombre", "numero_de_telefono", "linea_de_direccion", "codigo_postal", "ciudad", "provincia", "instrucciones"]
    template_name_suffix = "_update_form"
    
    def get_success_url(self):
        return reverse("user_configuration")


class DeleteDireccionView(LoginRequiredMixin, DeleteView):
    model = Direccion
    fields = ["nombre", "numero_de_telefono", "linea_de_direccion", "codigo_postal", "ciudad", "provincia", "instrucciones"]
    template_name_suffix = "_delete_form"
    
    def get_success_url(self):
        return reverse("user_configuration")


class CreateTarjetaView(LoginRequiredMixin, CreateView):
    model = Tarjeta
    fields = ["titular", "cc_number", "cc_expiry", "cc_code"]
    template_name_suffix = "_add_form"
    
    def form_valid(self, form):
        form.instance.cliente = Cliente.objects.get(user=self.request.user)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("user_configuration")


class UpdateTarjetaView(LoginRequiredMixin, UpdateView):
    model = Tarjeta
    fields = ["titular", "cc_number", "cc_expiry", "cc_code"]
    template_name_suffix = "_update_form"
    
    def get_success_url(self):
        return reverse("user_configuration")


class DeleteTarjetaView(LoginRequiredMixin, DeleteView):
    model = Tarjeta
    fields = ["titular", "cc_number", "cc_expiry", "cc_code"]
    template_name_suffix = "_delete_form"
    
    def get_success_url(self):
        return reverse("user_configuration")


class LoginView(FormView):
    template_name = "main/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        form.add_error(None, "Credenciales incorrectas!")
        return render(self.request, "main/login.html", context={"form": form})

    def get_success_url(self):
        next_url = self.request.GET.get('next', reverse('welcome'))
        return next_url

class UserCreateForm(UserCreationForm):
    captcha = CaptchaField()
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class RegisterView(FormView):
    template_name = "main/register.html"
    form_class = UserCreateForm

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        form.save()
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('welcome')


class LogoutView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = "welcome"


    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)
##############################################################