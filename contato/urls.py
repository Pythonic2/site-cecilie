from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ContatoView
urlpatterns = [
    path('contato/', ContatoView.as_view(), name='contato'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
