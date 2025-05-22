from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario 
from .forms import UsuarioForm, loginForm

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            usuario = Usuario.objects.filter(nome=form.cleaned_data['nome'], senha=form.cleaned_data['senha']).first()
            if usuario:
                print(usuario.nome)
                print(usuario.senha)
                return HttpResponse("usuario encontrado")
            else:
                print("nao foi")
                return HttpResponse("nao foi")
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