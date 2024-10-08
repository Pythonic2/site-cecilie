from django.urls import path
from .views import IndexView, filtrar_destaques
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('filter/<int:categoria_id>', filtrar_destaques, name='filter'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
