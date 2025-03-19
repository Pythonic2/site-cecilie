from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Produto, Categoria,Cidade
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from carrinho.models import Carrinho, ItemCarrinho
from authentication.models import Usuario
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import requests
from .models import Cidade
from authentication.models import Evento

def obter_taxa_por_cep_ou_cidade(cep=None, cidade_nome=None):

    try:
        if cidade_nome:
            cidade = Cidade.objects.get(nome=cidade_nome)
        elif cep:
            url = f"https://viacep.com.br/ws/{cep}/json/"
            response = requests.get(url)
            if response.status_code == 200:
                dados = response.json()
                cidade_nome = dados.get('localidade')
                cidade = Cidade.objects.get(nome=cidade_nome)
            else:
                return 0  # Sem taxa se a cidade não estiver cadastrada
        else:
            return 0  # Sem taxa se nem cidade nem CEP forem fornecidos

        return float(cidade.taxa)
    except Cidade.DoesNotExist:
        return 0  # Sem taxa se a cidade não estiver cadastrada


class CardapioView(TemplateView):
    template_name = 'shop.html'

    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categorias'] = Categoria.objects.all()
        context['titulo'] = 'Produtos'

        # Filtra os produtos por categoria (se houver)
        categoria_id = request.GET.get('categoria')
        if categoria_id:
            categoria = get_object_or_404(Categoria, id=categoria_id)
            produtos = Produto.objects.filter(categoria=categoria).order_by('-id')
        else:
            produtos = Produto.objects.all().order_by('-id')

        # Configuração da paginação
        paginator = Paginator(produtos, 9)  # 2 produtos por página
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context['produtos'] = page_obj
        context['categoria_atual'] = categoria_id

        # 🔹 Obtém o CEP do usuário (simulando um input ou vindo da sessão)
        #cep_usuario = request.GET.get("cep")  # Pega o CEP via GET (ou pode ser de um formulário)
        
        #if cep_usuario:
        evento = Evento.objects.last()
        taxa_cidade = obter_taxa_por_cep_ou_cidade(cidade_nome=request.session['cidade_selecionada'])  # Busca a taxa no banco
        request.session["taxa_cidade"] = taxa_cidade  # Armazena na sessão

        #else:
        taxa_cidade = request.session.get("taxa_cidade", 0)  # Se não houver CEP, usa 0

        # 🔹 Aplica a taxa sem acumular ao recarregar a página
        produtos_com_taxa = request.session.get("produtos_com_taxa", {})

        for produto in page_obj:
            if produto.id not in produtos_com_taxa:
                produtos_com_taxa[produto.id] = float(produto.valor) + float(taxa_cidade)  # ✅ Converte ambos

            produto.valor_com_taxa = produtos_com_taxa[produto.id]  # ✅ Usa valor já convertido

        request.session["produtos_com_taxa"] = {k: float(v) for k, v in produtos_com_taxa.items()}  # ✅ Converte tudo para float antes de salvar


        return render(request, self.template_name, context)


def htmx_list_produtos(request,categoria_id):
    context = {'produtos':Produto.objects.all().filter(categoria=categoria_id)} 

    return render(request, 'parciais/produtos/produtos.html' , context)