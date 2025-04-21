/**
 * Fort Wise Voice AI Assistant - Frontend JavaScript
 * 
 * This script handles:
 * - Voice recording
 * - Communication with backend API
 * - Conversation display
 * - Audio playback
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const recordButton = document.getElementById('recordButton');
    const stopButton = document.getElementById('stopButton');
    const resetButton = document.getElementById('resetButton');
    const statusText = document.getElementById('status-text');
    const recordingIndicator = document.getElementById('recording-indicator');
    const conversationContainer = document.getElementById('conversation');
    const audioPlayer = document.getElementById('audioPlayer');
    const audioPlayerContainer = document.getElementById('audio-player-container');
    
    // Variables
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    let stream;
    
    // Event Listeners
    recordButton.addEventListener('click', startRecording);
    stopButton.addEventListener('click', stopRecording);
    resetButton.addEventListener('click', resetConversation);
    
    // Check for microphone permissions
    async function checkMicrophonePermission() {
        try {
            await navigator.mediaDevices.getUserMedia({ audio: true });
            return true;
        } catch (err) {
            console.error('Microphone permission denied:', err);
            return false;
        }
    }
    
    // Start recording
    async function startRecording() {
        // Check if browser supports mediaDevices
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            showMessage('Your browser does not support audio recording.', 'system');
            return;
        }
        
        // Check for microphone permission
        const hasPermission = await checkMicrophonePermission();
        if (!hasPermission) {
            showMessage('Microphone access denied. Please allow microphone access to use this feature.', 'system');
            return;
        }
        
        try {
            // Reset audio chunks
            audioChunks = [];
            
            // Get media stream
            stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // Create media recorder
            mediaRecorder = new MediaRecorder(stream);
            
            // Event handlers
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            mediaRecorder.onstart = () => {
                // Update UI
                recordButton.classList.add('d-none');
                stopButton.classList.remove('d-none');
                statusText.textContent = 'Recording...';
                recordingIndicator.classList.remove('d-none');
                isRecording = true;
                
                // Auto-stop after 30 seconds (maximum duration)
                setTimeout(() => {
                    if (isRecording) {
                        stopRecording();
                    }
                }, 30000); // 30 seconds
            };
            
            mediaRecorder.onstop = async () => {
                // Update UI
                recordButton.classList.remove('d-none');
                stopButton.classList.add('d-none');
                statusText.textContent = 'Processing...';
                recordingIndicator.classList.add('d-none');
                isRecording = false;
                
                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
                
                // Process the recording
                await processRecording();
            };
            
            // Start recording
            mediaRecorder.start();
            
        } catch (err) {
            console.error('Error starting recording:', err);
            showMessage('Error starting recording: ' + err.message, 'system');
        }
    }
    
    // Stop recording
    function stopRecording() {
        if (mediaRecorder && isRecording) {
            mediaRecorder.stop();
        }
    }
    
    // Process the recording
    async function processRecording() {
        try {
            // Create blob from audio chunks
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            
            // Create form data
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.wav');
            
            // Send to backend
            const response = await fetch('/process_audio', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Display the conversation
            showMessage(data.text_input, 'user');
            showMessage(data.text_response, 'system');
            
            // Play audio response
            playAudioResponse(data.audio_url);
            
        } catch (err) {
            console.error('Error processing recording:', err);
            showMessage('Error processing your request: ' + err.message, 'system');
            statusText.textContent = 'Ready';
        }
    }
    
    // Play audio response
    function playAudioResponse(audioUrl) {
        statusText.textContent = 'Playing response...';
        
        // Set audio source
        audioPlayer.src = audioUrl;
        
        // Show audio player
        audioPlayerContainer.classList.remove('d-none');
        
        // Play audio
        audioPlayer.play();
        
        // Event listeners
        audioPlayer.onended = () => {
            statusText.textContent = 'Ready to listen';
        };
        
        audioPlayer.onerror = () => {
            statusText.textContent = 'Error playing audio';
            console.error('Error playing audio response');
        };
    }
    
    // Show message in conversation
    function showMessage(text, type) {
        // Create message elements
        const messageDiv = document.createElement('div');
        messageDiv.className = type === 'user' ? 'user-message' : 'system-message';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const paragraph = document.createElement('p');
        paragraph.textContent = text;
        paragraph.className = 'mb-0';
        
        const timestamp = document.createElement('div');
        timestamp.className = 'message-timestamp';
        
        const now = new Date();
        timestamp.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        // Assemble message
        contentDiv.appendChild(paragraph);
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timestamp);
        
        // Add to conversation
        conversationContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        conversationContainer.scrollTop = conversationContainer.scrollHeight;
    }
    
    // Reset conversation
    async function resetConversation() {
        try {
            const response = await fetch('/reset_context', {
                method: 'POST'
            });
            
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            
            // Clear conversation display
            conversationContainer.innerHTML = '';
            
            // Add welcome message
            const welcomeDiv = document.createElement('div');
            welcomeDiv.className = 'system-message';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            
            const paragraph = document.createElement('p');
            paragraph.textContent = 'Hello! I\'m the Fort Wise Voice AI Assistant. Ask me anything about Fort Wise using the microphone button below.';
            paragraph.className = 'mb-0';
            
            contentDiv.appendChild(paragraph);
            welcomeDiv.appendChild(contentDiv);
            
            conversationContainer.appendChild(welcomeDiv);
            
            // Hide audio player
            audioPlayerContainer.classList.add('d-none');
            
            // Reset status
            statusText.textContent = 'Ready to listen';
            
            // Show success message
            showMessage('Conversation has been reset.', 'system');
            
        } catch (err) {
            console.error('Error resetting conversation:', err);
            showMessage('Error resetting conversation: ' + err.message, 'system');
        }
    }
    
    // Helper function to format time
    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
});