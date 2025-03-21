# authentication/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
from django.core.validators import MinLengthValidator



class Usuario(AbstractUser):
    nome = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(auto_now_add=False, null=True, blank=True)
    cpf = models.CharField(
        max_length=11, 
        unique=True, 
        validators=[MinLengthValidator(11)],
        help_text="Informe um CPF válido sem pontos ou traços."
    )

   
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cpf

    

class Chopeira(models.Model):
    TIPO_CHOPEIRA_CHOICES = [
        ('bomba', 'Chopeira Bomba'),
        ('eletrica', 'Chopeira Elétrica'),
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOPEIRA_CHOICES, unique=True)

    def __str__(self):
        return dict(self.TIPO_CHOPEIRA_CHOICES).get(self.tipo, self.tipo)  # Retorna o rótulo correto

class Evento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cep = models.CharField(max_length=8, default=0)
    celular = models.CharField(max_length=11)
    bairro = models.CharField(max_length=100, default='None')
    endereco = models.CharField(max_length=100)
    data_evento = models.DateField(null=True)
    tipo_evento = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True, blank=True, default=' ')
    hora_evento = models.TimeField(null=True)
    #carrinho = models.CharField(max_length=50, default=0, unique=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    chopeiras = models.ManyToManyField(Chopeira)
    def __str__(self):
        return f"{self.tipo_evento} - {self.data_evento}"
