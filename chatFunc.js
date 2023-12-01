function sendMessage() {
    var input = document.getElementById('chat-input');
    var message = input.value.trim();
    if (message === '') return;

    var chatBox = document.getElementById('chat-box');
    var messageElement = document.createElement('div');
    messageElement.classList.add('chat-message');
    messageElement.textContent = message;
    chatBox.appendChild(messageElement); // Add the new message at the end (bottom)
    input.value = '';
    // Scroll to the latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById('chat-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

function sendMessageClick() {
    sendMessage();
}

// Retrieving the learning preferences
const learnPrefs = JSON.parse(localStorage.getItem('learningPreferences'))["learningPreferences"]; 