from django.db import models
from authentication.models import Usuario
def salvar_no_diretorio_do_user(instace, filename):
    return f'{instace.nome}/foto/{filename}'
# Create your models here.
class Parceiro(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=80)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    rua = models.CharField(max_length=130, blank=True, null=True)
    numero = models.CharField(max_length=5)
    imagem = models.ImageField(blank=True, upload_to=salvar_no_diretorio_do_user)

    def __str__(self):
        return self.nome
