from django.db import models


class Paciente(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    endereco = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome
