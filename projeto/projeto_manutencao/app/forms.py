from django import forms
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'tipo_perfil', 'senha']
    def save(self, commit=True):
        usuario = super().save(commit=False)
        senha_limpa = self.cleaned_data['senha']
        usuario.senha = make_password(senha_limpa)
        if commit:
            usuario.save()
        return usuario

class loginForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'senha']
