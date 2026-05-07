// Chatbot functionality
function toggleChatbot() {
    const widget = document.querySelector('.chatbot-widget');
    widget.classList.toggle('active');
}

function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    input.value = '';
    
    // Send to backend
    fetch('/chatbot/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            question: message,
            clinic_id: 1
        })
    })
    .then(response => response.json())
    .then(data => {
        addMessageToChat(data.response, 'bot');
    })
    .catch(error => {
        console.error('Error:', error);
        addMessageToChat('Sorry, I could not process your request.', 'bot');
    });
}

function addMessageToChat(text, sender) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageEl = document.createElement('div');
    messageEl.className = `message message-${sender}`;
    messageEl.textContent = text;
    messagesDiv.appendChild(messageEl);
    
    // Scroll to bottom
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Allow Enter key to send message
document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }
    
    // Close chatbot on close button
    const closeChat = document.querySelector('.close-chat');
    if (closeChat) {
        closeChat.addEventListener('click', toggleChatbot);
    }
});

// Add styling for messages
const style = document.createElement('style');
style.textContent = `
    .message {
        padding: 0.75rem;
        border-radius: 8px;
        max-width: 85%;
        word-wrap: break-word;
    }
    
    .message-user {
        align-self: flex-end;
        background: var(--primary-color);
        color: white;
        margin-left: auto;
    }
    
    .message-bot {
        align-self: flex-start;
        background: var(--surface-variant);
        color: var(--on-surface);
    }
`;
document.head.appendChild(style);
