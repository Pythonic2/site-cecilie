from django.shortcuts import render, redirect
from django.conf import settings
import logging
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from testemunho.models import Testemunho
from pagamento.models import Transacao
from django.utils.decorators import method_decorator
from notifications import send_email
import os
from dotenv import load_dotenv
from produto.models import Produto, Categoria
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from carrinho.models import Carrinho
from authentication.models import Usuario
from carrinho.models import ItemCarrinho
from produto.models import Produto
load_dotenv() 

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'

    method_decorator(cache_page(60 * 60 * 24))
    def get(self,request):
        produtos = Produto.objects.filter(destaque=True).order_by('-id')
        mais_vendidos = Produto.objects.filter(mais_vendido=True).order_by('-id')
        premiums = Produto.objects.filter(premium=True)
         
        usuario = request.user.username

        # Obtém o usuário atual
        user = Usuario.objects.get(username=usuario)

        carrinho = Carrinho.objects.filter(usuario=user).exclude(status='pago').last()
        categorias = Categoria.objects.all().order_by('-id')

        itens = ItemCarrinho.objects.filter(carrinho=carrinho)

        context = {'destaques':produtos,'categorias':categorias,'mais_vendidos':mais_vendidos,'produtos_p':premiums,'quantidade':sum(item.quantidade for item in itens)}
        return render(request, self.template_name, context)
    
        
@csrf_exempt
def filtrar_destaques(request, categoria_id):
    produtos_data = Produto.objects.filter(categoria=categoria_id, destaque=True)
    return render(request, 'parciais/destaques.html', {'destaques': produtos_data})