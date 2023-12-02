function displayMessage(message, className) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', className);
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
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
        if(data.error) {
            console.error('Error from server:', data.error);
        } else {
            displayMessage(data.response, 'received');
        }
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
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
