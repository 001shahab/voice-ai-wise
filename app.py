"""
Fort Wise Voice AI Assistant - Main Application

This is the main entry point for the Fort Wise Voice AI Assistant.
It initializes the Flask web application and sets up the routes.
"""

import os
import time
import uuid
from flask import Flask, request, jsonify, render_template, send_from_directory
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Import core modules
from core.voice_processor import VoiceProcessor
from utils.logging_utils import setup_logger

# Set up logging
setup_logger()
logger = logging.getLogger(__name__)

# Initialize the Flask application
app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize the voice processor
try:
    # Create necessary directories
    os.makedirs(os.path.join('data', 'recordings'), exist_ok=True)
    os.makedirs(os.path.join('data', 'faiss_index'), exist_ok=True)
    
    voice_processor = VoiceProcessor()
    logger.info("Voice processor initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize voice processor: {e}")
    raise

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    """
    Process audio from client.
    
    Expects audio data in the request, processes it through the voice pipeline,
    and returns the text response and audio URL.
    """
    try:
        # Check if audio file is in the request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        # Generate a unique filename for the audio
        filename = f"{str(uuid.uuid4())}.wav"
        save_path = os.path.join('data', 'recordings', filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save the file temporarily
        audio_file.save(save_path)
        
        logger.info(f"Audio saved to {save_path}, processing...")
        
        # Process the voice input
        text_input = voice_processor.speech_to_text(save_path)
        logger.info(f"Transcribed text: {text_input}")
        
        # Check if we got any text
        if not text_input or text_input.strip() == "":
            text_response = "I couldn't understand your question. Please try again."
            text_input = "[No speech detected]"
        else:
            # Get relevant context from knowledge base
            context = voice_processor.retrieve_context(text_input)
            
            # Generate response using LLM
            text_response = voice_processor.generate_response(text_input, context)
        
        logger.info(f"Generated response: {text_response}")
        
        # Convert text to speech
        audio_output_path = voice_processor.text_to_speech(text_response)
        
        # Get the relative URL for the audio file
        audio_url = f"/audio/{os.path.basename(audio_output_path)}"
        
        # Clean up input file
        try:
            os.remove(save_path)
        except Exception as e:
            logger.warning(f"Failed to delete temporary audio file: {e}")
        
        return jsonify({
            'text_input': text_input,
            'text_response': text_response,
            'audio_url': audio_url
        })
        
    except Exception as e:
        logger.error(f"Error processing audio: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve generated audio files."""
    return send_from_directory(os.path.join('data', 'recordings'), filename)

@app.route('/upload_knowledge', methods=['POST'])
def upload_knowledge():
    """
    Handle knowledge base file upload.
    
    Uploads and saves a text file to use as the knowledge base.
    """
    try:
        # Check if file is in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        if not file.filename.lower().endswith('.txt'):
            return jsonify({'error': 'Only .txt files are allowed'}), 400
        
        # Save the file
        file_path = os.path.join('data', 'knowledge_base.txt')
        file.save(file_path)
        
        # Reinitialize the knowledge base
        voice_processor.reinitialize_knowledge_base()
        
        logger.info(f"Knowledge base file uploaded and saved to {file_path}")
        
        return jsonify({
            'status': 'success',
            'message': 'Knowledge base file uploaded successfully',
            'filename': file.filename
        })
        
    except Exception as e:
        logger.error(f"Error uploading knowledge base file: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/reset_context', methods=['POST'])
def reset_context():
    """Reset the conversation context."""
    try:
        voice_processor.reset_context()
        return jsonify({'status': 'success', 'message': 'Context reset successfully'})
    except Exception as e:
        logger.error(f"Error resetting context: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    
    logger.info(f"Starting Fort Wise Voice AI Assistant on port {port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)