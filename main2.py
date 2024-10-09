from src.embedding_generator import EmbeddingGenerator

if __name__ == "__main__":
    azure_endpoint="https://cocria.openai.azure.com/"
    api_key="4c5bb55a31bf40f3ac36883dc5fdf110"
    api_version="2024-02-01"
    model_name = "text-embedding-ada-002"

    generator = EmbeddingGenerator(azure_endpoint, api_key, api_version)
    generator.generate_embeddings("src/data/documents/acessos.txt", model_name)
    generator.generate_embeddings("src/data/documents/suporte.txt", model_name)
    generator.generate_embeddings("src/data/documents/beneficios.txt", model_name)
    generator.generate_embeddings("src/data/documents/treinamentos.txt", model_name)