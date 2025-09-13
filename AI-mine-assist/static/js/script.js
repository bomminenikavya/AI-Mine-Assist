document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chatContainer');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    function addMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.className = `chat-message ${sender === 'You' ? 'user-message' : 'ai-message'}`;
        messageElement.textContent = `${sender}: ${message}`;
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function sendMessage(message) {
        try {
            const response = await fetch('/process-message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            if (response.ok) {
                const data = await response.json();
                addMessage('AI', data.response);
            } else {
                console.error('Server error:', response.statusText);
            }
        } catch (error) {
            console.error('Failed to send message:', error);
        }
    }

    function handleSendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessage('You', message);
            userInput.value = '';
            sendMessage(message);
        }
    }

    sendButton.addEventListener('click', handleSendMessage);

    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            handleSendMessage();
        }
    });
});