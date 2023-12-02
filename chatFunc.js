function displayMessage(message, className) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', className);
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight - chatBox.clientHeight; // Scrolls to the bottom
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (message === '') return;

    displayMessage(message, 'sent');
    callOpenAI(message);
    input.value = '';
}

document.getElementById('chat-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

function sendMessageClick() {
    sendMessage();
}

function callOpenAI(message) {
    showTypingIndicator();
    fetch('http://127.0.0.1:5000/get-response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        hideTypingIndicator();
        if(data.error) {
            console.error('Error from server:', data.error);
        } else {
            displayMessage(data.response, 'received');
        }
    })
    .catch(error => {
        hideTypingIndicator();
        console.error('There has been a problem with your fetch operation:', error);
    });
}
function showTypingIndicator() {
    const chatBox = document.getElementById('chat-box');
    const typingIndicator = document.createElement('div');
    typingIndicator.id = 'typing-indicator';
    typingIndicator.className = 'typing-indicator';
    typingIndicator.innerHTML = `
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    `;
    // Append the typing indicator to the chat box
    chatBox.appendChild(typingIndicator);
    // Make sure the chat box scrolls to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}



function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove(); // Removes the typing indicator from the DOM
        const chatBox = document.getElementById('chat-box');
        chatBox.scrollTop = chatBox.scrollHeight - chatBox.clientHeight; // Scrolls to the bottom
    }
}


    // fetch('http://127.0.0.1:5000/get-response', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({ message: message })
    // })
    // .then(response => {
    //     if (!response.ok) {
    //         throw new Error(`HTTP error! status: ${response.status}`);
    //     } else {
    //         return response.json();
    //     }
    // })
    // .then(data => {
    //     if (data.response) {
    //         displayMessage(data.response, 'received');
    //     } else if (data.error) {
    //         console.error('Error from the API:', data.error);
    //         // Optionally display a message to the user that an error occurred
    //     }
    // })
    // .catch((error) => {
    //     console.error('Error:', error);
    // });
