from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
# Create your models here.
class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=255, default='descreva a peça')
    disponivel = models.BooleanField(default=True)  # Use um valor padrão
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Usar DecimalField é melhor para preços
    quantidade = models.PositiveIntegerField(blank=True, null=True, default=1)  # Litros devem ser um valor positivo
    imagem = models.ImageField(upload_to='produtos')
    tamanho = models.CharField(max_length=3)
    def __str__(self):
        return self.nome

