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
from produto.models import Cidade
from produto.views import obter_taxa_por_cep_ou_cidade
from .models import ImagemSlide, EventoRealizado
load_dotenv() 

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'index.html'

    method_decorator(cache_page(60 * 60 * 24))
    def get(self,request):
        if not request.session.get('cidade_selecionada'):
            request.session['cidade_selecionada'] = 'Fortaleza'  # Define o valor padrão
            print(request.session['cidade_selecionada'])
        cidades = Cidade.objects.all()
        imagens = ImagemSlide.objects.all()
        context = {'cidades':cidades,'imagens':imagens}
        return render(request, self.template_name,context)
    
class HomeView(TemplateView):
    template_name = 'home.html'

    method_decorator(cache_page(60 * 60 * 24))
    def post(self, request, cidade_id):
        
        # cidade_id = request.POST.get('cidade')
        cidades = Cidade.objects.all()
        produtos = Produto.objects.filter(destaque=True).order_by('-id')
        cidade = get_object_or_404(Cidade, id=cidade_id)
        print(cidade)
        taxa_cidade = obter_taxa_por_cep_ou_cidade(cidade_nome=cidade)  # Busca a taxa no banco
        request.session["taxa_cidade"] = taxa_cidade  # Armazena na sessão
        
        #else:
        #taxa_cidade = request.session.get("taxa_cidade", 0)  # Se não houver CEP, usa 0

        # 🔹 Aplica a taxa sem acumular ao recarregar a página
        produtos_com_taxa = request.session.get("produtos_com_taxa", {})

        for produto in produtos:
            if produto.id not in produtos_com_taxa:
                produtos_com_taxa[produto.id] = float(produto.valor) + float(taxa_cidade)  # ✅ Converte ambos

            produto.valor_com_taxa = produtos_com_taxa[produto.id]  # ✅ Usa valor já convertido

        request.session["produtos_com_taxa"] = {k: float(v) for k, v in produtos_com_taxa.items()}  # ✅ Converte tudo para float antes de salvar
        request.session['cidade_selecionada'] = cidade.nome
        # Calcular os valores dos produtos com a taxa da cidade e armazenar na sessão
        # produtos = Produto.objects.all()
        # valores_com_taxa = {}
        # p_taxa = []
        # for produto in produtos:
        #     valor_com_taxa =float(produto.valor + cidade.taxa)
        #     valores_com_taxa[produto.id] = valor_com_taxa
        #     p_taxa.append(valores_com_taxa)
        # request.session['valores_com_taxa'] = valores_com_taxa
        feedbacks = Testemunho.objects.all().order_by('-id')
        context = {'destaques':produtos,'cidades':cidades,'cidade':cidade,'taxa':taxa_cidade,'feedbacks':feedbacks}
        eventos_realizados = EventoRealizado.objects.all().order_by('-id')
        context['eventos'] = eventos_realizados
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