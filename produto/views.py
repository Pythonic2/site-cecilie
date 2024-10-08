from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Produto, Categoria
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# Create your views here.
class CardapioView(TemplateView):
    """Renderiza o template do cardápio e retorna a quantidade de itens no carrinho"""

    template_name = 'shop.html'

    method_decorator(cache_page(60 * 60 * 24))
    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['produtos'] = Produto.objects.all().order_by('-id')
        context['categorias'] = Produto.objects.all()
        context['titulo'] = 'Produtos'


        return render(request, self.template_name, context)


def htmx_list_produtos(request,nome_categoria):
    context = {'produtos':Produto.objects.all().filter(categoria=nome_categoria)} 

    return render(request, 'parciais/produtos/produtos.html' , context)