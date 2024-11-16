from django.urls import path
from .views import CardapioView, htmx_list_produtos
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('produtos/', CardapioView.as_view(), name='produtos'),
    path('filtrar_produto/<int:categoria_id>', htmx_list_produtos, name='filtrar-produto'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
