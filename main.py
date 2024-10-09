from src.openaiassistant import OpenAIAssistant


azure_endpoint="https://cocria.openai.azure.com/"
api_key="4c5bb55a31bf40f3ac36883dc5fdf110"
api_version="2024-02-01"
chat_model = "gpt-4o-mini"
embedding_model = "text-embedding-ada-002"


if __name__ == '__main__':
    # Solicita o CPF e a empresa do usuário
    cpf = input("Por favor, insira seu CPF: ")
    empresa = input("Por favor, insira o nome da sua empresa: ")

    # Inicializa o assistente
    assistant = OpenAIAssistant(azure_endpoint, api_key, api_version, chat_model, embedding_model)

    # Obtém os documentos e os tópicos permitidos para o usuário
    permitted_documents, permitted_topics = assistant.get_permitted_documents(cpf, empresa)

    # Mapeia os documentos para os arquivos de embeddings correspondentes
    document_map = {
        "beneficios": "src/data/embeddings/beneficios_embeddings.pkl",
        "contratos": "src/data/embeddings/contratos_embeddings.pkl",
        "juridico": "src/data/embeddings/juridico_embeddings.pkl",
        "treinamentos": "src/data/embeddings/treinamentos_embeddings.pkl"
    }
    embedding_files = [document_map[doc] for doc in permitted_documents if doc in document_map]

    # Verifica se há documentos permitidos
    if not embedding_files:
        print("Você não tem permissão para acessar documentos.")
    else:
        # Carrega os embeddings permitidos
        assistant.load_embeddings(embedding_files)

        # Define o prompt com os tópicos permitidos
        assistant.set_prompt_with_topics(permitted_topics)

        # Loop para perguntas e respostas
        print("Pergunte algo sobre o documento ou digite 'sair' para encerrar.")
        while True:
            question = input("Sua pergunta: ")
            if question.lower() == "sair":
                print("Encerrando o assistente. Até a próxima!")
                break

            answer = assistant.ask_question(question)
            print("Resposta do assistente:", answer)
