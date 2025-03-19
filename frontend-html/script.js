// Initialize Monaco Editor
let editor;
require.config({ 
    paths: { 
        'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.36.1/min/vs'
    }
});

require(['vs/editor/editor.main'], function() {
    editor = monaco.editor.create(document.getElementById('editor'), {
        value: '',
        language: 'python',
        theme: 'vs-dark',
        minimap: { enabled: false },
        fontSize: 14,
        lineNumbers: 'on',
        scrollBeyondLastLine: false,
        automaticLayout: true,
        readOnly: false,
        scrollbar: {
            vertical: 'visible',
            horizontal: 'visible'
        },
        wordWrap: 'on',
        renderWhitespace: 'selection',
        tabSize: 4,
        insertSpaces: true,
        contextmenu: true,
        quickSuggestions: true,
        suggestOnTriggerCharacters: true,
        acceptSuggestionOnEnter: "on",
        tabCompletion: "on",
        wordBasedSuggestions: true,
        parameterHints: {
            enabled: true
        }
    });

    // Force editor to update its layout
    window.addEventListener('resize', function() {
        editor.layout();
    });
});

// Initialize Bootstrap Modal
let analysisModal;

document.addEventListener('DOMContentLoaded', function() {
    analysisModal = new bootstrap.Modal(document.getElementById('analysisModal'));
    
    // Handle modal close
    document.getElementById('analysisModal').addEventListener('hidden.bs.modal', function () {
        // Clear the modal content
        document.getElementById('analysisContent').innerHTML = '';
    });
});

// Navigation functions
function showHome() {
    document.getElementById('home-section').style.display = 'block';
    document.getElementById('interview-section').style.display = 'none';
    document.querySelector('.nav-link[onclick="showHome()"]').classList.add('active');
    document.querySelector('.nav-link[onclick="showInterview()"]').classList.remove('active');
}

function showInterview() {
    document.getElementById('home-section').style.display = 'none';
    document.getElementById('interview-section').style.display = 'block';
    document.querySelector('.nav-link[onclick="showHome()"]').classList.remove('active');
    document.querySelector('.nav-link[onclick="showInterview()"]').classList.add('active');
    
    // Force editor to update its layout when showing interview section
    if (editor) {
        setTimeout(() => editor.layout(), 100);
    }
}

// Form submission
document.getElementById('interview-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const role = document.getElementById('role').value;
    const skill = document.getElementById('skill').value;

    if (!role || !skill) {
        alert('Please select both role and skill');
        return;
    }

    try {
        console.log('Starting interview with:', { role, skill }); // Debug log
        const response = await fetch('http://localhost:5000/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Role': role,
                'Skill': skill,
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Server error:', errorData); // Debug log
            throw new Error(errorData.error || 'Failed to start interview');
        }

        const data = await response.json();
        console.log('Received response:', data); // Debug log
        localStorage.setItem('currentQuestion', data.message);
        
        // Add the question to chat and speak it
        addMessage(data.message, 'ai');
        
        // Show interview section
        showInterview();
        
        // Set editor language based on skill
        if (editor) {
            if (skill.toLowerCase() === 'python') {
                monaco.editor.setModelLanguage(editor.getModel(), 'python');
            } else if (skill.toLowerCase() === 'javascript' || skill.toLowerCase() === 'react') {
                monaco.editor.setModelLanguage(editor.getModel(), 'javascript');
            } else if (skill.toLowerCase() === 'java') {
                monaco.editor.setModelLanguage(editor.getModel(), 'java');
            } else if (skill.toLowerCase() === 'c++') {
                monaco.editor.setModelLanguage(editor.getModel(), 'cpp');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage(error.message || 'Failed to start interview. Please try again.', 'ai');
    }
});

// Text-to-Speech functionality
let ttsEnabled = true; // Set to true by default
let speechSynthesis = window.speechSynthesis;
let currentUtterance = null;

// Check if browser supports speech synthesis
if (!window.speechSynthesis) {
    console.error('Speech synthesis not supported in this browser');
    document.getElementById('tts-toggle').style.display = 'none';
}

// Initialize text-to-speech toggle button
document.getElementById('tts-toggle').addEventListener('click', function() {
    ttsEnabled = !ttsEnabled;
    const button = this;
    const icon = button.querySelector('i');
    
    if (ttsEnabled) {
        button.classList.remove('btn-outline-primary');
        button.classList.add('btn-primary');
        icon.classList.remove('fa-volume-up');
        icon.classList.add('fa-volume-mute');
        button.title = 'Disable Text-to-Speech';
    } else {
        button.classList.remove('btn-primary');
        button.classList.add('btn-outline-primary');
        icon.classList.remove('fa-volume-mute');
        icon.classList.add('fa-volume-up');
        button.title = 'Enable Text-to-Speech';
        // Stop any ongoing speech
        if (currentUtterance) {
            speechSynthesis.cancel();
        }
    }
});

// Function to speak text with a slight delay
function speakText(text) {
    if (!ttsEnabled) return;
    
    // Cancel any ongoing speech
    if (currentUtterance) {
        speechSynthesis.cancel();
    }
    
    // Create new utterance
    currentUtterance = new SpeechSynthesisUtterance(text);
    
    // Configure speech settings
    currentUtterance.rate = 1.2;  // Increased speed for faster speech
    currentUtterance.pitch = 1.0; // Normal pitch
    currentUtterance.volume = 1.0; // Full volume
    
    // Add error handling
    currentUtterance.onerror = function(event) {
        console.error('Speech synthesis error:', event.error);
    };
    
    // Add a small delay before speaking
    setTimeout(() => {
        speechSynthesis.speak(currentUtterance);
    }, 100);
}

// Modify the addMessage function to include text-to-speech
function addMessage(content, type) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = content;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    // Speak AI messages when TTS is enabled
    if (type === 'ai' && ttsEnabled) {
        speakText(content);
    }
}

async function askQuestion() {
    const input = document.getElementById('question-input');
    const question = input.value.trim();
    const code = editor ? editor.getValue() : '';
    const submitButton = input.nextElementSibling;

    if (!question) {
        addMessage("Please enter your question", 'ai');
        return;
    }

    if (!code) {
        addMessage("Please write some code before asking a question", 'ai');
        return;
    }

    try {
        // Add loading state
        const originalButtonContent = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        submitButton.disabled = true;

        // Add user's question to chat first
        addMessage(question, 'user');

        const response = await fetch('http://localhost:5000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                input: question,
                code: code
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || 'Failed to send question');
        }

        const data = await response.json();
        
        // Add AI's response to chat and speak it
        addMessage(data.response, 'ai');
        
        // Clear input
        input.value = '';
    } catch (error) {
        console.error('Error:', error);
        addMessage(error.message || 'Failed to send question. Please try again.', 'ai');
    } finally {
        // Always restore button state, even if there's an error
        submitButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        submitButton.disabled = false;
    }
}

async function submitCode() {
    const code = editor ? editor.getValue() : '';
    
    if (!code) {
        addMessage("Please provide your code before submitting", 'ai');
        return;
    }

    try {
        // Add a loading message
        addMessage("Analyzing your code submission...", 'ai');
        
        const response = await fetch('http://localhost:5000/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                expected_duration: 30,
                candidates_duration: 30
            })
        });

        if (!response.ok) {
            throw new Error('Failed to submit code');
        }

        const data = await response.json();
        
        // Clear the loading message
        const messagesDiv = document.getElementById('chat-messages');
        if (messagesDiv.lastChild && messagesDiv.lastChild.textContent === "Analyzing your code submission...") {
            messagesDiv.removeChild(messagesDiv.lastChild);
        }
        
        // Format and display the analysis report in the chat
        const report = data.feedback;
        
        // Add a separator message
        addMessage("📊 Code Analysis Report", 'ai separator');
        
        // Format and add the report sections
        if (typeof report === 'string') {
            // If report is a string, split it into sections
            const sections = report.split('\n\n');
            sections.forEach(section => {
                if (section.trim()) {
                    const lines = section.split('\n');
                    const title = lines[0].replace(/^\d+\.\s*\*\*|\*\*:$/g, '').trim();
                    const content = lines.slice(1).join('\n').trim();
                    addMessage(`📌 ${title}:\n${content}`, 'ai');
                }
            });
        } else {
            // If report is an object, format it directly
            addMessage(`📌 Code Analysis:\n${JSON.stringify(report, null, 2)}`, 'ai');
        }
        
        // End the interview session
        await fetch('http://localhost:5000/end', {
            method: 'POST'
        });
        
        // Add a message indicating the interview has ended
        addMessage("Interview session completed. Thank you for participating!", 'ai');
        
        // Scroll to the bottom of the chat
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    } catch (error) {
        console.error('Error:', error);
        // Remove the loading message if it exists
        const messagesDiv = document.getElementById('chat-messages');
        if (messagesDiv.lastChild && messagesDiv.lastChild.textContent === "Analyzing your code submission...") {
            messagesDiv.removeChild(messagesDiv.lastChild);
        }
        addMessage("Failed to analyze code. Please try again.", 'ai');
    }
}

function formatReportSection(title, content) {
    // Split content into paragraphs
    const paragraphs = content.split('\n').filter(p => p.trim());
    
    return `
        <div class="report-section">
            <h5>${title}</h5>
            ${paragraphs.map(p => `<p>${p}</p>`).join('')}
        </div>
    `;
} 