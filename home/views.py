from django.shortcuts import render
from django.http import HttpResponse
import json
from src.openaiassistant import OpenAIAssistant
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import CustomUser
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import get_user
from empresa.models import Topico
import os
from dotenv import load_dotenv
load_dotenv()

azure_endpoint = os.getenv('AZURE_ENDPOINT')
api_key = os.getenv('API_KEY')
api_version = os.getenv('VERSION')
chat_model = os.getenv('CHAT_MODEL')
embedding_model = os.getenv('EMBEDDING_MODEL')

openai = OpenAIAssistant(azure_endpoint, api_key, api_version, chat_model, embedding_model)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'chat.html'
    def get(self, request):
        usuario = get_user(request)
        praticas = usuario.praticas.prefetch_related('topicos') # Otimiza a consulta
        # Cria uma lista para armazenar os nomes dos tópicos
        praticas_com_topicos = []
        temas_permitidos = []

        for pratica in praticas:
            for topico in pratica.topicos.all():
                praticas_com_topicos.append(topico.nome)
                temas_permitidos.append(topico.nome_formatado)  
        listas = [f'src/data/embeddings/{topico}_embeddings.pkl' for topico in temas_permitidos]
        openai.load_embeddings(listas)

        openai.set_prompt_with_topics(temas_permitidos)

        context = {
            'usuario': usuario.first_name,
            'praticas_com_topicos': set(praticas_com_topicos),  # Passa a lista de tópicos para o contexto
        }
        
        return render(request, self.template_name, context)
        

       

def htmx_enviar_mensagem(request):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            msg_user = data.get('msg', '').strip()
            if msg_user:
                response = openai.ask_question(msg_user)
                bot_response = f"""
                    <div class='message-wrapper'>
                        <div class='bot-avatar'><img src='/static/img/assistant_avatar.png'></div>
                        <div class='bot-message'>
                        {response}
                        <div class="message-actions">
                            <i class="fas fa-thumbs-up"></i> <!-- Ícone de curtir -->
                            <i class="fas fa-thumbs-down"></i> <!-- Ícone de não curtir -->
                            <i class="fas fa-copy"></i> <!-- Ícone de copiar -->
                        </div>
                        </div>
                    </div>
                """
                return HttpResponse(bot_response) 
            else:
                return HttpResponse("Mensagem vazia.", status=400)  
        except json.JSONDecodeError:
            return HttpResponse("Erro ao processar JSON.", status=400)
    else:
        return HttpResponse("Método inválido.", status=405)

