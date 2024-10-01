document.addEventListener('DOMContentLoaded', () => {
    const chatOutput = document.getElementById('chat-output');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    const botMessages = [
        "Welcome to KemisDigital Advanced Digital Marketing Strategies Waitlist! 🎉",
        "Our upcoming event is in January 2025. Are you interested in joining our waitlist?",
        "Great! Please provide your email address.",
        "Thank you! Now, please enter your phone number.",
        "Excellent! Lastly, what's your full name?",
        "Thank you for your interest! We've added you to our waitlist. We'll contact you with more details about the January 2025 event soon!"
    ];

    let currentStep = 0;
    let userInfo = {
        email: '',
        phone: '',
        fullName: ''
    };

    function displayMessage(content, isUser = false) {
        const messageElement = document.createElement('div');
        messageElement.textContent = isUser ? `You: ${content}` : `Bot: ${content}`;
        messageElement.className = `message ${isUser ? 'user' : 'bot'}`;
        chatOutput.appendChild(messageElement);
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }

    function handleUserInput() {
        const userMessage = userInput.value.trim();
        if (userMessage) {
            displayMessage(userMessage, true);
            processUserInput(userMessage);
            userInput.value = '';
        }
    }

    function processUserInput(input) {
        switch (currentStep) {
            case 1:
                if (input.toLowerCase() === 'yes') {
                    currentStep++;
                    setTimeout(() => displayMessage(botMessages[2]), 500);
                } else {
                    displayMessage("No problem! If you change your mind, feel free to start over.");
                    currentStep = 0;
                }
                break;
            case 2:
                if (validateEmail(input)) {
                    userInfo.email = input;
                    currentStep++;
                    setTimeout(() => displayMessage(botMessages[3]), 500);
                } else {
                    displayMessage("That doesn't look like a valid email. Please try again.");
                }
                break;
            case 3:
                if (validatePhone(input)) {
                    userInfo.phone = input;
                    currentStep++;
                    setTimeout(() => displayMessage(botMessages[4]), 500);
                } else {
                    displayMessage("That doesn't look like a valid phone number. Please try again.");
                }
                break;
            case 4:
                userInfo.fullName = input;
                currentStep++;
                registerUser();
                break;
        }
    }

    function validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function validatePhone(phone) {
        return /^\+?[\d\s-]{10,}$/.test(phone);
    }

    function registerUser() {
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userInfo),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayMessage(botMessages[5]);
            } else {
                displayMessage("Oops! Something went wrong. Please try again later.");
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            displayMessage("Oops! Something went wrong. Please try again later.");
        });
    }

    sendButton.addEventListener('click', handleUserInput);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleUserInput();
        }
    });

    // Start the conversation
    displayMessage(botMessages[0]);
    setTimeout(() => {
        displayMessage(botMessages[1]);
        currentStep = 1;
    }, 1000);
});
