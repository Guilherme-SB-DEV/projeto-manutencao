from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('usuario/<int:id>/', views.usuario, name='usuario'),
    path('chamado/<int:id>/', views.chamado, name='chamado'),
    path('recuperacao/', views.recuperacao, name='recuperacao'),
    path('atende/<int:id>/<int:id_chamado>', views.atende, name='atende'),
    path('chat/<int:id>/<int:id_chamado>', views.chat, name='chat'),
    path('alterSenha/<int:token>/auth/<int:id>', views.alterSenha, name='alterSenha')
    # path('usuario/<int:id_usuario>/chamado/listar', views.chamado_listar, name='chamado_listar')
]