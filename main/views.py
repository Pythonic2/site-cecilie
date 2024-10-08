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

load_dotenv() 
logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'

    method_decorator(cache_page(60 * 60 * 24))
    def get(self,request):
        produtos = Produto.objects.filter(destaque=True).order_by('-id')
        mais_vendidos = Produto.objects.filter(mais_vendido=True).order_by('-id')
        categorias = Categoria.objects.all().order_by('-id')
        context = {'destaques':produtos,'categorias':categorias,'mais_vendidos':mais_vendidos,'quantidade':10}
        return render(request, self.template_name, context)
    
        
@csrf_exempt
def filtrar_destaques(request, categoria_id):
    produtos_data = Produto.objects.filter(categoria=categoria_id, destaque=True)
    return render(request, 'parciais/destaques.html', {'destaques': produtos_data})