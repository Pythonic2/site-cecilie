from django.db import models

class ImagemSlide(models.Model):
    imagem = models.ImageField(upload_to='slides/')
    tipo = models.CharField(max_length=50, default='Evento')

    def __str__(self):
        return self.tipo



class EventoRealizado(models.Model):
    tipo_evento = models.CharField(max_length=30, default='esse texto aparecerá abaixo da imagem', blank=True)
    imagem = models.ImageField(upload_to='eventos/')
    data = models.DateField(auto_now_add=False)
    def __str__(self):
        return self.tipo_evento