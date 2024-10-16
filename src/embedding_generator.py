import os
import fitz  # PyMuPDF para ler PDFs
import pickle
from openai import AzureOpenAI
#import docx

class EmbeddingGenerator:
    def __init__(self, azure_endpoint: str, api_key: str, api_version: str, embedding_dir="data/embeddings"):
        # Define o caminho absoluto para a pasta src/data/embeddings
        self.embedding_dir = os.path.join(os.path.dirname(__file__), embedding_dir)
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )

        # Cria a pasta de embeddings se não existir
        if not os.path.exists(self.embedding_dir):
            os.makedirs(self.embedding_dir)

    def load_document(self, file_path: str):
        """Carrega o conteúdo de um arquivo .txt ou .pdf e retorna como uma lista de trechos."""
        ext = os.path.splitext(file_path)[1].lower()
        document_content = ""
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                document_content = file.read()
        elif ext == ".pdf":
            with fitz.open(file_path) as pdf:
                for page_num in range(pdf.page_count):
                    page = pdf[page_num]
                    document_content += page.get_text()
        else:
            raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf.")

        # Divide o conteúdo em trechos para gerar embeddings individuais
        return document_content.split('\n\n')

    def generate_embedding(self, text, model_name):
        """Gera um embedding para o texto fornecido usando Azure OpenAI."""
        response = self.client.embeddings.create(
            input=text,  # Texto a ser transformado em embedding
            model=model_name  # Nome do deployment do modelo de embedding no Azure
        )
        return response.data[0].embedding

    def generate_embeddings(self, file_path: str, model_name: str):
        """Gera e salva embeddings para cada trecho do documento."""
        document_chunks = self.load_document(file_path)
        embeddings = []

        for chunk in document_chunks:
            embedding = self.generate_embedding(chunk, model_name)
            embeddings.append({"text": chunk, "embedding": embedding})

        # Salva os embeddings em um arquivo .pkl
        file_name = os.path.basename(file_path).split('.')[0] + "_embeddings.pkl"
        with open(os.path.join(self.embedding_dir, file_name), "wb") as f:
            pickle.dump(embeddings, f)

        print(f"Embeddings gerados e salvos em {file_name}")


if __name__ == "__main__":
    
    azure_endpoint = os.getenv('AZURE_ENDPOINT')
    api_key = os.getenv('API_KEY')
    api_version = os.getenv('VERSION')
    chat_model = os.getenv('CHAT_MODEL')
    model_name = os.getenv('EMBEDDING_MODEL')

    generator = EmbeddingGenerator(azure_endpoint, api_key, api_version)
    generator.generate_embeddings("data/documents/acessos.txt", model_name)
    generator.generate_embeddings("data/documents/suporte.txt", model_name)
    generator.generate_embeddings("data/documents/beneficios.txt", model_name)
    generator.generate_embeddings("data/documents/treinamentos.txt", model_name)
