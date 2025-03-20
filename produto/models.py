from django.db import models
import requests

class Cidade(models.Model):
    nome = models.CharField(max_length=50)
    taxa = models.DecimalField(max_digits=10, decimal_places=2)
    frete = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255, default='descreva o produto/serviço')
    disponivel = models.BooleanField(default=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    litros = models.PositiveIntegerField(blank=True, null=True)
    imagem = models.ImageField(upload_to='media/', blank=True, null=True, default=None)
    servico = models.BooleanField(default=False)
    disponivel = models.BooleanField(default=True)
    destaque = models.BooleanField(default=False)
    promo = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)
    mais_vendido = models.BooleanField(default=False)
    def __str__(self):
        return self.nome

    

