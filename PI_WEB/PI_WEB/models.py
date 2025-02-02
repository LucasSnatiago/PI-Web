from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Ferramenta(models.Model):
    nome = models.CharField(max_length=40)
    descricao = models.TextField()
    tipo = models.CharField(max_length=10)
    imagem = models.FileField()

class Usuario(models.Model):
    ra = models.CharField(max_length=15, primary_key=True)
    nome = models.CharField(max_length=40)
    emprestimos = models.ManyToManyField('Reserva', through='Emprestimo', through_fields=('usuario', 'reserva'), blank=True)

class Servidor(Usuario, AbstractBaseUser):
    funcao = models.CharField(max_length=1, choices=(("P", "Profesosr"),("B", "Bolsista")), null=False)
    ferramentas_reservadas = models.ManyToManyField(Ferramenta, through='Reserva', blank=True)
    USERNAME_FIELD = 'ra'

class Aluno(Usuario):
    curso = models.CharField(max_length=7)

class Reserva(models.Model):
    ferramenta = models.ForeignKey(Ferramenta, on_delete=models.DO_NOTHING)
    servidor = models.ForeignKey(Servidor, on_delete=models.DO_NOTHING)
    data = models.DateTimeField(auto_now_add=True, primary_key=True)

class Emprestimo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name='emprestimos_feitos')
    reserva = models.ForeignKey(Reserva, on_delete=models.DO_NOTHING)
    dataRetirada = models.DateTimeField(auto_now_add=True, blank=True)
    data_devolucao = models.DateTimeField(blank=True, null=True)
    responsavel_devolucao = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True, null=True)
    supervisor_devolucao = models.ForeignKey(Servidor, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='emprestimos_supervisionados')
