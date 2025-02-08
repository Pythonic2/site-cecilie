from django.db import models

# Create your models here.
class Parceiro(models.Model):
    nome = models.CharField(max_length=80)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    rua = models.CharField(max_length=130, blank=True, null=True)
    numero = models.CharField(max_length=5)

    def __str__(self):
        return self.nome
