from django.urls import path
from .views import LoginView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
  
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
