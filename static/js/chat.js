class ChatWidget {
  constructor() {
    this.messages = [];
    this.sessionId = null;
    this.messagesContainer = document.getElementById('chat-messages');
    this.initializeEventListeners();
  }

  initializeEventListeners() {
    const sendButton = document.getElementById('send-button');
    sendButton.addEventListener('click', () => this.sendMessage());

    const inputField = document.getElementById('chat-input');
    inputField.addEventListener('keypress', (event) => {
      if (event.key === 'Enter') {
        this.sendMessage();
      }
    });

    const closeButton = document.getElementById('close-button');
    closeButton.addEventListener('click', () => this.toggleChat());

    const minimizeButton = document.getElementById('minimize-button');
    minimizeButton.addEventListener('click', () => this.toggleMinimize());

    const chatButton = document.getElementById('chat-widget-button');
    chatButton.addEventListener('click', () => this.toggleChat());
  }

  async sendMessage() {
    const inputField = document.getElementById('chat-input');
    const message = inputField.value.trim();
    if (!message) return;

    this.addMessage(message, 'user');
    inputField.value = '';

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: this.messages,
        }),
      });
      const data = await response.json();
      this.addMessage(data.response, 'bot');
    } catch (error) {
      console.error('Error:', error);
      this.addMessage('Lo siento, hubo un error al procesar tu mensaje.', 'bot');
    }
  }

  addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;

    const linkedContent = content.replace(
      /(https?:\/\/[^\s]+)/g,
      '<a href="$1" target="_blank">$1</a>'
    );

    messageDiv.innerHTML = linkedContent;
    this.messagesContainer.appendChild(messageDiv);
    this.scrollToBottom();

    // Agregar el mensaje al historial
    this.messages.push({ role: type, content: content });
  }

  toggleChat() {
    const chatContainer = document.getElementById('chat-widget-container');
    chatContainer.classList.toggle('hidden');
  }

  toggleMinimize() {
    const chatContainer = document.getElementById('chat-widget-container');
    chatContainer.classList.toggle('minimized');
  }

  scrollToBottom() {
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const chatWidget = new ChatWidget();
});
