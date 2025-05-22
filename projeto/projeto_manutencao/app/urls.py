from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
]