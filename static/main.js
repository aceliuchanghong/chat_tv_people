// Voice Cloning Section
const recordBtn = document.getElementById('record-btn');
const cloneBtn = document.getElementById('clone-btn');

recordBtn.addEventListener('click', async () => {
    try {
        // TODO: Implement voice recording functionality
        console.log('Recording voice sample...');
    } catch (error) {
        console.error('Error recording voice:', error);
    }
});

cloneBtn.addEventListener('click', async () => {
    try {
        // TODO: Implement voice cloning functionality
        console.log('Cloning voice...');
    } catch (error) {
        console.error('Error cloning voice:', error);
    }
});

// Character Background Section
const backgroundInput = document.getElementById('background-input');
const saveBackgroundBtn = document.getElementById('save-background');
let currentCharacterId = null;

saveBackgroundBtn.addEventListener('click', async () => {
    const background = backgroundInput.value.trim();
    if (background) {
        try {
            const response = await fetch('/api/save_background', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ background })
            });
            
            const data = await response.json();
            if (data.success) {
                currentCharacterId = data.character_id;
                alert('Character background saved successfully!');
            } else {
                alert('Error saving background: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error saving background:', error);
            alert('Failed to save background. Please try again.');
        }
    } else {
        alert('Please enter a character background');
    }
});

// Chat Interface Section
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const chatHistory = document.getElementById('chat-history');

async function loadChatHistory() {
    if (!currentCharacterId) return;
    
    try {
        const response = await fetch(`/api/get_chat_history/${currentCharacterId}`);
        const data = await response.json();
        if (data.success) {
            chatHistory.innerHTML = '';
            data.history.forEach(msg => {
                addMessageToHistory(msg.message, msg.is_user === 1);
            });
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

sendBtn.addEventListener('click', async () => {
    const message = chatInput.value.trim();
    if (message) {
        if (!currentCharacterId) {
            alert('Please save a character background first');
            return;
        }
        
        try {
            const response = await fetch('/api/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    character_id: currentCharacterId,
                    message: message
                })
            });
            
            const data = await response.json();
            if (data.success) {
                chatInput.value = '';
                addMessageToHistory(message, true);
                addMessageToHistory(data.response, false);
            } else {
                alert('Error sending message: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error sending message:', error);
            alert('Failed to send message. Please try again.');
        }
    } else {
        alert('Please enter a message');
    }
});

// Load chat history when character is selected
backgroundInput.addEventListener('change', loadChatHistory);

// Utility function to add messages to chat history
function addMessageToHistory(message, isUser = true) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', isUser ? 'user-message' : 'character-message');
    messageElement.textContent = message;
    chatHistory.appendChild(messageElement);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}
