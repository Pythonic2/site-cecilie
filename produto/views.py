from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Produto, Categoria
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from carrinho.models import Carrinho, ItemCarrinho
from authentication.models import Usuario
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


class CardapioView(TemplateView):
    """Renderiza o template do cardápio e retorna a quantidade de itens no carrinho"""
    template_name = 'shop.html'

    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = request.user.username

        # Obtém o usuário atual
        user = Usuario.objects.get(username=usuario)
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
        paginator = Paginator(produtos, 2)  # 2 produtos por página
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Adiciona o objeto de página e categoria atual ao contexto
        context['produtos'] = page_obj
        context['categoria_atual'] = categoria_id

        # Carrinho e itens
        carrinho = Carrinho.objects.filter(usuario=user).exclude(status='pago').last()
        itens = ItemCarrinho.objects.filter(carrinho=carrinho)
        context['quantidade'] = sum(item.quantidade for item in itens)

        return render(request, self.template_name, context)


def htmx_list_produtos(request,categoria_id):
    print("entrou aqui")
    context = {'produtos':Produto.objects.all().filter(categoria=categoria_id)} 

    return render(request, 'parciais/produtos/produtos.html' , context)