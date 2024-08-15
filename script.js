document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatBox = document.getElementById('chat-box');
   

    chatForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const userMessage = chatInput.value.trim();

        if (userMessage) {
            appendMessage('You', userMessage);
            chatInput.value = '';
            sendMessage(userMessage);
        }
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    }

    function sendMessage(message) {
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                user_id: userId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                appendMessage('Bot', data.message);
            } else {
                appendMessage('Bot', 'Sorry, I didn\'t get that.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('Bot', 'Sorry, something went wrong.');
        });
    }
});
