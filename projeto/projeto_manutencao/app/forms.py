from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'tipo_perfil', 'senha']

class loginForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'senha']