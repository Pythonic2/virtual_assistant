import os
import pickle
import faiss
import numpy as np
import sqlite3
from openai import AzureOpenAI
from src.prompt import prompt

class OpenAIAssistant:
    def __init__(self, azure_endpoint: str, api_key: str, api_version: str, chat_model: str, embedding_model: str, embedding_dim: int = 1536):
        """Inicializa o cliente Azure OpenAI, o índice FAISS, e o histórico de conversas."""
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
        self.chat_model = chat_model
        self.embedding_model = embedding_model
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.documents = []
        self.prompt = prompt
        self.chat_history = []

    def get_permitted_documents(self, cpf: str, empresa: str):
        """Consulta o banco de dados e retorna os documentos permitidos e os tópicos correspondentes."""
        conn = sqlite3.connect('src/data/access_control.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT documentos FROM permissions WHERE cpf = ? AND empresa = ?
        ''', (cpf, empresa))
        result = cursor.fetchone()
        conn.close()

        if result:
            # Divide a string de documentos em uma lista
            permitted_documents = result[0].split(',')
            # Mapear os documentos para os tópicos correspondentes
            document_map = {
                "beneficios": "benefícios",
                "contratos": "acessos",
                "juridico": "suporte",
                "treinamentos": "treinamentos"
            }
            permitted_topics = [document_map[doc] for doc in permitted_documents if doc in document_map]
            return permitted_documents, permitted_topics
        else:
            return [], []

    def load_embeddings(self, embedding_files):
        """Carrega múltiplos arquivos de embeddings e os adiciona ao índice FAISS."""
        for file_path in embedding_files:
            with open(file_path, "rb") as f:
                data = pickle.load(f)
                embeddings = np.array([item["embedding"] for item in data]).astype('float32')
                self.index.add(embeddings)
                self.documents.extend([item["text"] for item in data])
        print("Embeddings de múltiplos arquivos carregados e indexados.")

    def set_prompt_with_topics(self, topics):
        """Atualiza o prompt para incluir os tópicos de conversa permitidos."""
        topics_str = ", ".join(topics)
        self.prompt = f"{prompt}\n\nVocê pode conversar sobre os seguintes assuntos: {topics_str}."

    def retrieve_context(self, question: str, top_k: int = 3):
        """Recupera os trechos mais relevantes para a pergunta usando embeddings."""
        query_embedding = self.client.embeddings.create(
            input=question,
            model=self.embedding_model  # Usa o modelo de embeddings
        ).data[0].embedding
        _, indices = self.index.search(np.array([query_embedding]).astype('float32'), top_k)
        return "\n\n".join([self.documents[idx] for idx in indices[0]])

    def ask_question(self, question: str):
        """Usa o contexto recuperado e o histórico de conversa para gerar uma resposta com Azure OpenAI."""
        if not self.index.is_trained:
            return "Embeddings não carregados. Por favor, carregue os embeddings primeiro."

        # Recupera o contexto relevante
        context = self.retrieve_context(question)

        # Adiciona o prompt e o contexto ao histórico
        self.chat_history.append({"role": "system", "content": self.prompt})
        self.chat_history.append({"role": "system", "content": f"Contexto relevante:\n{context}"})
        
        # Adiciona a pergunta do usuário ao histórico
        self.chat_history.append({"role": "user", "content": question})

        try:
            # Faz a chamada ao modelo de chat Azure OpenAI com o histórico de conversa
            response = self.client.chat.completions.create(
                model=self.chat_model,  # Usa o modelo de chat
                messages=self.chat_history
            )
            # Extrai e formata a resposta do assistente
            answer = response.choices[0].message.content.strip()

            # Adiciona a resposta do assistente ao histórico
            self.chat_history.append({"role": "assistant", "content": answer})

            return answer
        except Exception as e:
            return f"Erro ao consultar a API Azure OpenAI: {e}"
