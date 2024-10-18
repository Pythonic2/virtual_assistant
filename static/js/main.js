const inputField = document.querySelector('#message-input');
const sendButton = document.querySelector('.send-btn');
const chatContainer = document.querySelector('#chat-container');

// Função para rolar automaticamente para o final do chat
function autoScroll() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function sendMessage() {
    const message = inputField.value.trim();

    if (message) {
        const userMessageHTML = `
            <div class="message-wrapper">
                <div class="user-message">${message}</div>
            </div>
        `;
        document.querySelector('#chat-container').insertAdjacentHTML('beforeend', userMessageHTML);
        autoScroll();  // Rola o chat para o final após o envio da mensagem

        inputField.value = '';

        // Use a URL gerada no template
        fetch(chatMessageURL, {
            method: 'POST',
            
            body: JSON.stringify({ msg: message })
        })
        .then(response => response.text())
        .then(data => {
            document.querySelector('#chat-container').insertAdjacentHTML('beforeend', data);
            autoScroll();  // Rola o chat para o final após a resposta do bot
        })
        .catch(error => console.error('Erro:', error));
    } else {
        console.error('Mensagem vazia');
    }
}

sendButton.addEventListener('click', sendMessage);
inputField.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});
