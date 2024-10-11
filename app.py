import streamlit as st
from src.openaiassistant import OpenAIAssistant
import base64

# Configurações da Azure OpenAI
azure_endpoint = "https://cocria.openai.azure.com/"
api_key = "4c5bb55a31bf40f3ac36883dc5fdf110"
api_version = "2024-02-01"
chat_model = "gpt-4o-mini"
embedding_model = "text-embedding-ada-002"

# Função para inicializar o assistente
@st.cache_resource
def initialize_assistant():
    return OpenAIAssistant(azure_endpoint, api_key, api_version, chat_model, embedding_model)

assistant = initialize_assistant()

# Função para converter a imagem em base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Gera a string base64 da imagem do avatar
avatar_base64 = get_base64_image("src/images/assistant_avatar.png")

# Barra lateral para iniciar novo chat
st.sidebar.title("Opções")
if st.sidebar.button("Iniciar novo chat"):
    st.session_state.clear()
    st.session_state["messages"] = [("assistant", "Olá! Aqui é o Henrique, assistente virtual do RH. Consigo te ajudar com dúvidas sobre acessos, benefícios, suporte e treinamentos. Mas antes, me fala o seu CPF para que eu possa encontrar o seu cadastro?")]
    st.session_state["authenticated"] = False
    st.session_state["cpf"] = ""
    st.session_state["empresa"] = ""

# Configuração da interface estilo ChatGPT
st.title("Henrique 🤖")
st.markdown("### Seu assistente virtual do RH!")

# Adiciona o CSS para o avatar personalizado
st.markdown(
    """
    <style>
    .assistant-avatar {
        display: inline-block;
        vertical-align: middle;
        margin-right: 10px;
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }
    .assistant-response {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicialização do estado da sessão
if "messages" not in st.session_state:
    st.session_state["messages"] = [("assistant", "Olá! Aqui é o Henrique, assistente virtual do RH. Consigo te ajudar com dúvidas sobre acessos, benefícios, suporte e treinamentos. Mas antes, me fala o seu CPF para que eu possa encontrar o seu cadastro?")]
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "cpf" not in st.session_state:
    st.session_state["cpf"] = ""
if "empresa" not in st.session_state:
    st.session_state["empresa"] = ""

# Captura o input do usuário
user_input = st.chat_input("Digite aqui...")

if user_input:
    if not st.session_state["cpf"]:
        # Armazena o CPF e solicita o nome da empresa
        st.session_state["cpf"] = user_input
        st.session_state["messages"].append(("user", user_input))
        st.session_state["messages"].append(("assistant", "Obrigado! Agora, poderia informar o nome da sua empresa?"))
    elif not st.session_state["empresa"]:
        # Armazena o nome da empresa e realiza a autenticação
        st.session_state["empresa"] = user_input
        st.session_state["messages"].append(("user", user_input))

        cpf = st.session_state["cpf"]
        empresa = st.session_state["empresa"]

        # Verifica permissões
        permitted_documents, permitted_topics = assistant.get_permitted_documents(cpf, empresa)

        document_map = {
            "beneficios": "src/data/embeddings/beneficios_embeddings.pkl",
            "contratos": "src/data/embeddings/contratos_embeddings.pkl",
            "juridico": "src/data/embeddings/juridico_embeddings.pkl",
            "acessos": "src/data/embeddings/acessos_embeddings.pkl",
            "treinamentos": "src/data/embeddings/treinamentos_embeddings.pkl"
        }
        embedding_files = [document_map[doc] for doc in permitted_documents if doc in document_map]

        if not embedding_files:
            st.session_state["messages"].append(("assistant", "Desculpe, você não tem permissão para acessar documentos."))
        else:
            # Carrega os embeddings e define o prompt com tópicos permitidos
            assistant.load_embeddings(embedding_files)
            assistant.set_prompt_with_topics(permitted_topics)
            st.session_state["authenticated"] = True

            # Mensagem de boas-vindas com tópicos permitidos
            topics_message = f"Qual a sua dúvida? Eu consigo te auxiliar sobre: {', '.join(permitted_topics)}."
            st.session_state["messages"].append(("assistant", topics_message))
    elif st.session_state["authenticated"]:
        # Adiciona a pergunta do usuário ao histórico e obtém a resposta do assistente
        st.session_state["messages"].append(("user", user_input))
        answer = assistant.ask_question(user_input)
        st.session_state["messages"].append(("assistant", answer))

# Exibição das mensagens finais com avatar personalizado para o assistente
for role, message in st.session_state["messages"]:
    if role == "assistant":
        st.markdown(
            f"""
            <div class="assistant-response">
                <img src="data:image/png;base64,{avatar_base64}" class="assistant-avatar">
                <span>{message}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        with st.chat_message(role):
            st.markdown(message)
