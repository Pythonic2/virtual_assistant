from django.urls import path
from .views import HomeView, htmx_enviar_mensagem
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('enviar-mensagem/', htmx_enviar_mensagem, name='enviar-mensagem'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)