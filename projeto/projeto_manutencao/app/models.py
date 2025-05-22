# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categoria(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Categoria'


class Chamado(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    prioridade = models.CharField(db_column='Prioridade', max_length=100, blank=True, null=True)  # Field name made lowercase.
    data_conclusao = models.DateField(db_column='Data_Conclusao', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=100, blank=True, null=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=100, blank=True, null=True)  # Field name made lowercase.
    data_abertura = models.DateField(db_column='Data_Abertura', blank=True, null=True)  # Field name made lowercase.
    titulo = models.CharField(db_column='Titulo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fk_categoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='fk_Categoria_Id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Chamado'


class ClienteAbre(models.Model):
    fk_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='fk_Usuario_Id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cliente_abre'


class Mensagem(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    conteudo = models.CharField(db_column='Conteudo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fk_chamado = models.ForeignKey(Chamado, models.DO_NOTHING, db_column='fk_Chamado_Id', blank=True, null=True)  # Field name made lowercase.
    fk_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='fk_Usuario_Id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mensagem'


class Notificacao(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fk_chamado = models.ForeignKey(Chamado, models.DO_NOTHING, db_column='fk_Chamado_Id', blank=True, null=True)  # Field name made lowercase.
    fk_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='fk_Usuario_Id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Notificacao'


class Usuario(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    senha = models.CharField(db_column='Senha', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tipo_perfil = models.CharField(db_column='Tipo_Perfil', max_length=100, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Usuario'


class TecnicoAtende(models.Model):
    fk_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='fk_Usuario_Id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tecnico_atende'
