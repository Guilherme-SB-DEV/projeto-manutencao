from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario
from .models import Chamado
from .models import ClienteAbre
from .models import TecnicoAtende
from .models import Mensagem
from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from .forms import UsuarioForm, loginForm
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
import yagmail

yag = yagmail.SMTP("guilhermebra93@gmail.com", "sriz ybmm okxy kyme")


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def login(request):
    if request.method == "POST":
        form = loginForm(request.POST)
        if form.is_valid():
            usuario = Usuario.objects.filter(nome=form.cleaned_data["nome"]).first()

            if usuario and check_password(form.cleaned_data["senha"], usuario.senha):

                print(usuario.nome)
                print(usuario.senha)
                return redirect("usuario", id=usuario.id)

            else:
                return render(
                    request,
                    "app/login.html",
                    {"form": form, "error": "Usuario ou senha invalidos"},
                )
    else:
        return render(request, "app/login.html")


# def chamado_listar(request, id_usuario):
#     return render(request, 'app/chamado_listar.html', {'chamados': chamados})


def cadastro(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            print(form.data.get("nome"))
            print(form.data.get("tipo_perfil"))
            print(form.data.get("senha"))
            form.save()
            return redirect("login")
        else:
            return render(request, "app/cadastro.html", {"msg": "erro ao cadastrar"})
    else:
        return render(request, "app/cadastro.html")


def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, "app/listar_usuarios.html", {"usuarios": usuarios})


from django.db.models import Q  # Import necessário


def usuario(request, id):
    usuario = Usuario.objects.get(id=id)
    chamados = []

    status_filtro = request.GET.get("status")
    pesquisa = request.GET.get("pesquisa")

    if usuario.tipo_perfil == "cliente":
        cliente_abres = ClienteAbre.objects.filter(fk_usuario=id)
        chamados_ids = cliente_abres.values_list("fk_chamado_id", flat=True)
        chamados = Chamado.objects.filter(id__in=chamados_ids)

    elif usuario.tipo_perfil in ["tecnico", "admin"]:
        chamados = Chamado.objects.all()

    if status_filtro:
        chamados = chamados.filter(status=status_filtro)

    if pesquisa:
        chamados = chamados.filter(
            Q(titulo__icontains=pesquisa) | Q(descricao__icontains=pesquisa)
        )

    if usuario.tipo_perfil == "admin":
        usuarios = Usuario.objects.all()
        tecnicos = usuarios.filter(tipo_perfil="tecnico")
        tecnicos_obj = []
        for tecnico in tecnicos:
            tecnico_atendes = TecnicoAtende.objects.filter(fk_usuario=tecnico.id)
            atendimentos = 0
            tempo_total = 0

            for tecnico_atende in tecnico_atendes:
                chamado = Chamado.objects.filter(id=tecnico_atende.fk_chamado.id, status="concluido").first()
                if chamado and chamado.data_conclusao and chamado.data_abertura:
                    atendimentos += 1
                    tempo_total += (chamado.data_conclusao - chamado.data_abertura).total_seconds() / 3600

            tecnicos_obj.append({
                "tecnico": tecnico,
                "atendimentos": atendimentos,
                "tempo": round(tempo_total, 2)
            })

        quantidade_aberto = Chamado.objects.filter(status__iexact="aberto").count()
        quantidade_em_andamento = Chamado.objects.filter(status="em andamento").count()
        quantidade_concluido = Chamado.objects.filter(status="concluido").count()
        quantidade_cancelado = Chamado.objects.filter(status="cancelado").count()


        soma = 0
        for chamado in chamados:
            if chamado.status.lower() == "concluido" and chamado.data_conclusao and chamado.data_abertura:
                diferenca = chamado.data_conclusao - chamado.data_abertura
                print(diferenca)
                soma += diferenca.total_seconds() / 3600  # converte segundos para horas

        quantidade_concluido = Chamado.objects.filter(status__iexact="concluido").count()
        print(quantidade_concluido)
        if quantidade_concluido > 0:
            media = soma / quantidade_concluido
        else:
            media = 0
        print(media)


        return render(
            request,
            "app/usuario.html",
            {
                "usuario": usuario,
                "clientes": usuarios.filter(tipo_perfil="cliente"),
                "tecnicos_obj": tecnicos_obj,
                "chamados": chamados,
                "atendimentos": atendimentos,
                "abertos": quantidade_aberto,
                "em_andamento": quantidade_em_andamento,
                "concluidos": quantidade_concluido,
                "cancelados": quantidade_cancelado,
                "media": media
            },
        )

    return render(
        request, "app/usuario.html", {"usuario": usuario, "chamados": chamados}
    )


def chamado(request, id):
    descricao = request.POST.get("descricao")
    titulo = request.POST.get("titulo")
    prioridade = request.POST.get("prioridade")
    categoria = request.POST.get("categoria")

    usuario = Usuario.objects.get(id=id)

    yag.send(
        to="g.braga@ba.estudante.senai.br",
        subject="Chamado aberto com sucesso!",
        contents="Chamado aberto com sucesso! Recebemos sua solicitação e ela foi registrada em nosso sistema. Um de nossos técnicos analisará o chamado em breve e você poderá acompanhar o andamento diretamente pelo sistema. Lembre-se: você pode visualizar o status, atualizar informações ou encerrar o chamado a qualquer momento acessando a seção Acompanhar Chamados. Obrigado por utilizar o SGCT – estamos aqui para ajudar!",
    )

    chamado = Chamado(
        descricao=descricao,
        titulo=titulo,
        prioridade=prioridade,
        data_abertura=datetime.now(),
        status="aberto",
        categoria=categoria,
    )
    chamado.save()
    cliente_abre = ClienteAbre(fk_chamado=chamado, fk_usuario=usuario)
    cliente_abre.save()
    return redirect("usuario", id=usuario.id)


def atende(request, id, id_chamado):
    status = request.POST.get("status")
    tempo = request.POST.get("tempo")

    chamado = Chamado.objects.get(id=id_chamado)
    tecnico = Usuario.objects.get(id=id)
    if status == "em andamento":
        chamado.tempo_estimado = tempo

    chamado.status = status
    if status == "concluido":
        chamado.data_conclusao = datetime.now()
    chamado.save()

    clienteAbre = ClienteAbre.objects.filter(fk_chamado=chamado.id).first()
    if clienteAbre:
        cliente = clienteAbre.fk_usuario  # Já é um objeto Usuario

        yag.send(
            to=cliente.email,
            subject="Chamado concluido",
            contents="O status do seu chamado foi alterado para: "
            + status
            + "\nCom um tempo estimado de: "
            + tempo
            + " horas",
        )

    tecnico_atende = TecnicoAtende(fk_chamado=chamado, fk_usuario=tecnico)
    tecnico_atende.save()
    return redirect("usuario", id=id)


def chat(request, id, id_chamado):
    usuario = get_object_or_404(Usuario, id=id)
    chamado = get_object_or_404(Chamado, id=id_chamado)

    # Verificação de permissão
    autorizado = False
    if usuario.tipo_perfil == "tecnico":
        autorizado = TecnicoAtende.objects.filter(
            fk_chamado=chamado, fk_usuario=usuario
        ).exists()
    elif usuario.tipo_perfil == "cliente":
        autorizado = ClienteAbre.objects.filter(
            fk_chamado=chamado, fk_usuario=usuario
        ).exists()
    
    if not autorizado:
        return render(
            request,
            "app/erro.html",
            {"mensagem": "Você não tem permissão para acessar este chat."},
        )

    # Se for POST, salva a nova mensagem
    if request.method == "POST":
        conteudo = request.POST.get("mensagem")
        if conteudo:
            Mensagem.objects.create(
                conteudo=conteudo,
                fk_chamado=chamado,
                fk_usuario=usuario,
                tempo_envio=timezone.now(),
            )
        return redirect(
            "chat", id=usuario.id, id_chamado=chamado.id
        )  # evita reenvio com refresh

    # Requisição GET: exibir mensagens
    mensagens = Mensagem.objects.filter(fk_chamado=chamado).order_by("tempo_envio")

    return render(
        request,
        "app/chat.html",
        {"usuario": usuario, "chamado": chamado, "mensagens": mensagens},
    )


def recuperacao(request):
    if request.method == "POST":
        email = request.POST.get("email")
        usuario = Usuario.objects.get(email=email)
        if usuario:
            yag.send(
                to=usuario.email,
                subject="Recuperacao de Senha",
                contents="Sua senha é: " + usuario.senha,
            )

        return redirect("login", mensagem="Sua senha foi enviada pelo seu email.")
    else:
        return render(request, "app/recuperacao.html")
