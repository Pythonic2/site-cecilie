from django.contrib import admin
from .models import Produto,Categoria,Cidade

admin.site.register(Produto)
admin.site.register(Categoria)
admin.site.register(Cidade)
