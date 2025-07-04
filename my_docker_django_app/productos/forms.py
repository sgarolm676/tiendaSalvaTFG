from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, DireccionEnvio, TarjetaPago, Producto, ComentarioProducto

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PersonalizacionForm(forms.Form):
    COLOR_CHOICES = [
        ('Rojo', 'Rojo'), ('Azul', 'Azul'), ('Verde', 'Verde'),
        ('Negro', 'Negro'), ('Blanco', 'Blanco'), ('Gris', 'Gris'),
        ('Amarillo', 'Amarillo'), ('Morado', 'Morado')
    ]

    PERSONALIZACION_POSICION = [
        ('lateral', 'Lateral'),
        ('trasera', 'Trasera')
    ]

    PERSONALIZACION_TIPO = [
        ('frase', 'Frase'),
        ('imagen', 'Imagen')
    ]

    color = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    posicion = forms.ChoiceField(choices=PERSONALIZACION_POSICION, widget=forms.RadioSelect)
    tipo = forms.ChoiceField(choices=PERSONALIZACION_TIPO, widget=forms.RadioSelect)
    frase = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    imagen = forms.ImageField(required=False)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen', 'bio']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

class DireccionEnvioForm(forms.ModelForm):
    class Meta:
        model = DireccionEnvio
        exclude = ['usuario']
        fields = '__all__'
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TarjetaPagoForm(forms.ModelForm):
    class Meta:
        model = TarjetaPago
        exclude = ['usuario']
        fields = '__all__'
        widgets = {
            'titular': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'expiracion': forms.TextInput(attrs={'class': 'form-control'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control'}),
        }
class ComentarioProductoForm(forms.ModelForm):
    class Meta:
        model = ComentarioProducto
        fields = ['texto', 'estrellas']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estrellas': forms.Select(choices=[(i, f"{i} estrellas") for i in range(1, 6)], attrs={'class': 'form-select'}),
        }