from django.db import models

class ImagemSlide(models.Model):
    imagem = models.ImageField(upload_to='slides/')
    tipo = models.CharField(max_length=50, default='Evento')

    def __str__(self):
        return self.tipo
    