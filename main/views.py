from django.shortcuts import render, redirect
from django.conf import settings
import logging
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from testemunho.models import Testemunho
from django.utils.decorators import method_decorator
from notifications import send_email
import os
from dotenv import load_dotenv
from produto.models import Produto
from django.views.decorators.csrf import csrf_exempt
from produto.models import Produto
load_dotenv() 

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'

    method_decorator(cache_page(60 * 60 * 24))
    def get(self,request):
        produtos = Produto.objects.filter(destaque=True).order_by('-id')
        mais_vendidos = Produto.objects.filter(mais_vendido=True).order_by('-id')
        # premiums = Produto.objects.filter(premium=True)
        
        # usuario = request.user.username

        # # Obtém o usuário atual
        # user = Usuario.objects.get(username=usuario)

        # carrinho = Carrinho.objects.filter(usuario=user).exclude(status='pago').last()
        # categorias = Categoria.objects.all().order_by('-id')

        # itens = ItemCarrinho.objects.filter(carrinho=carrinho)
        #context = {'destaques':produtos,'categorias':categorias,'mais_vendidos':mais_vendidos,'produtos_p':premiums,'quantidade':sum(item.quantidade for item in itens)}
        feedbacks = Testemunho.objects.all().order_by('-id')
        context = {'destaques':produtos,'feedbacks':feedbacks,'mais_vendidos':mais_vendidos}
        return render(request, self.template_name,context)
    
    
        
@csrf_exempt
def filtrar_destaques(request, categoria_id):
    produtos_data = Produto.objects.filter(categoria=categoria_id, destaque=True)
    return render(request, 'parciais/destaques.html', {'destaques': produtos_data})





# class GaleriaView(TemplateView):
#     template_name = 'galeria.html'

#     def get(self, request):
#         eventos = EventoRealizado.objects.all().order_by('-id')
#         print(f'-------count {eventos.count()}')
#         categorias = CategoriaEvento.objects.all()
#         context = {'eventos': eventos, 'categorias': categorias}
#         return render(request, self.template_name, context)

# def is_admin_or_in_group(user):
#     """Verifica se o usuário é um superusuário ou pertence a um grupo específico."""
#     return user.is_superuser or user.groups.filter(name='nome_do_grupo').exists()

# @method_decorator(login_required, name='dispatch')
# @method_decorator(user_passes_test(is_admin_or_in_group), name='dispatch')
# class GaleriaCreateView(TemplateView):
#     template_name = 'cadastra_imagens_evento.html'
    
#     def get(self, request):
#         categorias = CategoriaEvento.objects.all()
#         context = {'categorias': categorias}
#         return render(request, self.template_name, context)
     
#     def post(self, request, *args, **kwargs):
#         if request.method == 'POST':
#             # Obtém o ID da categoria e o nome do evento do request
#             categoria_id = request.POST.get('categoria')
#             nome_evento = request.POST.get('nome')

#             # Cria e salva a instância do EventoRealizado
#             evento = EventoRealizado.objects.create(categoria_id=categoria_id, nome=nome_evento)

#             # Obtém a lista de imagens do request
#             images = request.FILES.getlist('images')
#             images.reverse()
#             # Cria objetos ImagemEvento para cada imagem enviada
#             try:
#                 for image in images:
#                     img = ImagemEvento(evento=evento, imagem=image)
#                     img.save()
#                 # Redireciona para a galeria após o upload
#                 return redirect('cad_fotos')
#             except Exception as e:
#                 print(e)

#         # Caso não seja um POST, renderiza a página com um erro ou a página de galeria
#         return render(request, self.template_name, {'error': 'Método não suportado'})