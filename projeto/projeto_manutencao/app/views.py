from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario 
from .forms import UsuarioForm, loginForm
from django.contrib.auth.hashers import make_password, check_password

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            usuario = Usuario.objects.filter(nome=form.cleaned_data['nome']).first()
            

            if usuario and check_password(form.cleaned_data['senha'], usuario.senha):
            
                print(usuario.nome)
                print(usuario.senha)
                return render('usuario', id_usuario=usuario.id)
            
            else:
                print("nao foi")
                return render(request, 'app/login.html', {'form': form, 'error': 'Usuario ou senha invalidos'})
    else:
        return render(request, 'app/login.html')


def cadastro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            print(form.data.get('nome'))
            print(form.data.get('tipo_perfil'))
            print(form.data.get('senha'))
            form.save()
            return HttpResponse("foi")
        else:
            return HttpResponse("nao foi")
    else:
        return render(request, 'app/cadastro.html')


def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'app/listar_usuarios.html', {'usuarios': usuarios})

def usuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)

    return render(request, 'app/usuario.html', {'usuario': usuario})