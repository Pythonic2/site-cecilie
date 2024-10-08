from django.urls import path
from .views import CardapioView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('produtos/', CardapioView.as_view(), name='produtos'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
