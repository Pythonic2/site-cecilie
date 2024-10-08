from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Produto, Categoria
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from carrinho.models import Carrinho, ItemCarrinho
from authentication.models import Usuario
# Create your views here.
class CardapioView(TemplateView):
    """Renderiza o template do cardápio e retorna a quantidade de itens no carrinho"""

    template_name = 'shop.html'

    method_decorator(cache_page(60 * 60 * 24))
    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = request.user.username

    # Obtém o usuário atual
        user = Usuario.objects.get(username=usuario)
        context['produtos'] = Produto.objects.all().order_by('-id')
        context['categorias'] = Produto.objects.all()
        context['titulo'] = 'Produtos'
        carrinho = Carrinho.objects.filter(usuario=user).exclude(status='pago').last()
        itens = ItemCarrinho.objects.filter(carrinho=carrinho)

        context['quantidade'] = itens.count()


        return render(request, self.template_name, context)


def htmx_list_produtos(request,nome_categoria):
    context = {'produtos':Produto.objects.all().filter(categoria=nome_categoria)} 

    return render(request, 'parciais/produtos/produtos.html' , context)